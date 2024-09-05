from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
from typing import Tuple, List, Optional
import ssl


def connect_to_vsphere(host: str, user: str, pwd: str):
    """
    Connects to the vSphere environment and returns a ServiceInstance object.
    """
    # Disable SSL certificate verification (not recommended for production)
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_NONE

    try:
        # Connect to vCenter Server
        si = SmartConnect(host=host, user=user, pwd=pwd, sslContext=context)
        # Retrieve content
        content = si.RetrieveContent()
        print(f"Connected successfully to vCenter at {host}")

        return si, content
    except Exception as e:
        print(f"Failed to connect to vCenter: {str(e)}")
        return


def disconnect_from_vsphere(si):
    """
    Disconnects from the vSphere environment.
    """
    if si:
        try:
            Disconnect(si)
            return "Disconnected successfully from vCenter."
        except Exception as e:
            return f"Failed to disconnect from vCenter: {str(e)}"
    return "No connection found to disconnect."


def get_all_vms(si, content) -> Tuple[List[vim.VirtualMachine], List[str]]:
    """
    Retrieves a list of all virtual machines (VMs) in the vSphere environment.

    Args:
        si: The ServiceInstance object representing the connection to vCenter.

    Returns:
        str: A list of VM names in the vSphere environment.

    Raises:
        Exception: If there is an issue with retrieving the VMs.
    """
    vm_names = []
    try:
        # Create container view for Virtual Machines
        container = content.viewManager.CreateContainerView(
            content.rootFolder, [vim.VirtualMachine], True
        )

        # List all VMs
        vms = container.view

        # Check if any VMs were retrieved
        if not vms:
            # print("No VMs found!")
            return

        # Print the names of the VMs
        for vm in vms:
            # print(f"VM Name: {vm.name}")
            vm_names.append(vm.name)

        print(f"VMs in the vSphere environment: {', '.join(vm_names)}")

        return vms, vm_names
    except Exception as e:
        raise Exception(f"Failed to retrieve VMs: {str(e)}")


def get_vm_details(vm) -> dict:
    """
    Retrieves details of a specific virtual machine (VM) in the vSphere environment, including:
        - Operating system
        - Resource allocations (CPU, memory, disk)
        - Network configuration (IP, network adapter settings)
        - Operational status (power state, connection state, overall status)

    Args:
        vm: The vim.VirtualMachine object representing the VM in vCenter.

    Returns:
        dict: A dictionary containing VM details.
    """
    try:
        # Initialize the VM details dictionary
        vm_info = {}

        # Get basic VM info
        vm_info["name"] = vm.summary.config.name
        vm_info["operating_system"] = vm.summary.config.guestFullName

        # Resource allocations
        vm_info["cpu"] = vm.config.hardware.numCPU
        vm_info["memory_mb"] = vm.config.hardware.memoryMB

        # Disk allocations
        vm_info["disks"] = []
        for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualDisk):
                disk_info = {
                    "label": device.deviceInfo.label,
                    "capacity_gb": device.capacityInKB
                    / (1024 * 1024),  # Convert KB to GB
                }
                vm_info["disks"].append(disk_info)

        # Network configuration
        vm_info["networks"] = []
        for net in vm.guest.net:
            network_info = {
                "network_name": net.network,
                "ip_addresses": net.ipAddress,
                "mac_address": net.macAddress,
            }
            vm_info["networks"].append(network_info)

        # Operational Status
        vm_info["power_state"] = vm.runtime.powerState
        vm_info["connection_state"] = vm.runtime.connectionState
        vm_info["overall_status"] = vm.summary.overallStatus

        return vm_info

    except Exception as e:
        raise Exception(f"Failed to retrieve details for VM: {str(e)}")


def get_all_vm_details(content) -> list:
    """
    Retrieves details of all virtual machines (VMs) in the vSphere environment.

    Args:
        content: The vim.ServiceContent object representing the vSphere content.

    Returns:
        list: A list of dictionaries, each containing details of a VM, including:
              - Operating system
              - Resource allocations (CPU, memory, disk)
              - Network configuration (IP, network adapter settings)

    Raises:
        Exception: If an error occurs during retrieval of VM details.
    """
    vm_details_list = []

    # Traverse all VMs in the vSphere inventory
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.VirtualMachine], True
    )
    for vm in container.view:
        vm_details = get_vm_details(vm)
        vm_details_list.append(vm_details)

    container.Destroy()

    return vm_details_list


def verify_vm_not_running(
    vm: vim.VirtualMachine, warm_migration_supported: bool = False
) -> Optional[str]:
    """
    Ensures that a single VM is not running if 'warm' migration is not supported.

    Args:
        vm (vim.VirtualMachine): The VM object to check.
        warm_migration_supported (bool): Whether warm migration (live migration) is supported.

    Returns:
        Optional[str]: A message confirming the VM's power state or an error message if applicable.
    """
    try:
        power_state = vm.runtime.powerState

        if warm_migration_supported:
            return f"VM '{vm.name}' is currently {power_state}. No action needed."

        if power_state == vim.VirtualMachinePowerState.poweredOn:
            # Power off the VM
            task = vm.PowerOff()
            task.WaitForCompletion()
            return (
                f"VM '{vm.name}' was powered on and has been powered off for migration."
            )
        else:
            return f"VM '{vm.name}' is already powered off."

    except Exception as e:
        return f"Failed to manage power state for VM '{vm.name}': {str(e)}"


def verify_vms_not_running(
    vm_names: List[str],
    si,
    content,
    warm_migration_supported: bool = False,
) -> None:
    """
    Ensures that all VMs in the list are not running if 'warm' migration is not supported.

    Args:
        vm_names (List[str]): A list of VM names targeted for migration.
        warm_migration_supported (bool): Whether warm migration (live migration) is supported.

    Returns:
        None
    """
    try:

        for vm_name in vm_names:
            vm = get_vm_by_name(content, vm_name)
            if not vm:
                print(f"VM '{vm_name}' not found.")
                continue

            # Ensure VM is not running if warm migration is not supported
            result = verify_vm_not_running(vm, warm_migration_supported)
            print(result)

    except Exception as e:
        print(f"Error during the operation: {str(e)}")

    finally:
        if si:
            disconnect_from_vsphere(si)


def get_vm_by_name(content, vm_name: str) -> Optional[vim.VirtualMachine]:
    """
    Retrieves a specific virtual machine (VM) by its name from the vSphere environment.

    Args:
        content: The ServiceContent object representing the vSphere content.
        vm_name (str): The name of the virtual machine to search for.

    Returns:
        Optional[vim.VirtualMachine]: The VM object if found, or None if the VM is not found.
    """
    try:
        # Create a container view for Virtual Machines
        container = content.viewManager.CreateContainerView(
            content.rootFolder, [vim.VirtualMachine], True
        )

        # Iterate over all VMs in the container and search for the VM by name
        for vm in container.view:
            if vm.name == vm_name:
                return vm

        # Return None if the VM was not found
        return None

    except Exception as e:
        raise Exception(f"Failed to retrieve VM by name '{vm_name}': {str(e)}")

    finally:
        if container:
            container.Destroy()


def find_vm_by_name(si, vm_name: str) -> str:
    """
    Finds a specific virtual machine (VM) by its name in the vSphere environment.

    Args:
        si: The ServiceInstance object representing the connection to vCenter.
        vm_name: The name of the VM to find.

    Returns:
        str: A message indicating the VM was found, or an error message if not found.

    Raises:
        Exception: If there is an issue with finding the VM or it doesn't exist.
    """

    try:
        content = si.RetrieveContent()

        for datacenter in content.rootFolder.childEntity:
            for vm in datacenter.vmFolder.childEntity:
                if vm.name == vm_name:
                    return f"VM '{vm_name}' found. Power state: {vm.runtime.powerState}"

        raise Exception(f"VM '{vm_name}' not found.")

    except Exception as e:
        raise Exception(f"Failed to find VM: {str(e)}")


def power_on_vm(si, vm_name: str) -> str:
    """
    Powers on a specific virtual machine (VM) by its name in the vSphere environment.

    Args:
        si: The ServiceInstance object representing the connection to vCenter.
        vm_name: The name of the VM to power on.

    Returns:
        str: A message indicating that the VM was powered on successfully or if it was already powered on.

    Raises:
        Exception: If there is an issue powering on the VM.
    """

    try:
        vm = find_vm_by_name(si, vm_name)

        if vm.runtime.powerState != vim.VirtualMachinePowerState.poweredOn:
            vm.PowerOn()
            return f"VM '{vm_name}' powered on."
        else:
            return f"VM '{vm_name}' is already powered on."

    except Exception as e:
        raise Exception(f"Failed to power on VM: {str(e)}")


def power_off_vm(si, vm_name: str) -> str:
    """
    Powers off a specific virtual machine (VM) by its name in the vSphere environment.

    Args:
        si: The ServiceInstance object representing the connection to vCenter.
        vm_name: The name of the VM to power off.

    Returns:
        str: A message indicating that the VM was powered off successfully or if it was already powered off.

    Raises:
        Exception: If there is an issue powering off the VM.
    """

    try:
        vm = find_vm_by_name(si, vm_name)

        if vm.runtime.powerState != vim.VirtualMachinePowerState.poweredOff:
            vm.PowerOff()
            return f"VM '{vm_name}' powered off."
        else:
            return f"VM '{vm_name}' is already powered off."

    except Exception as e:
        raise Exception(f"Failed to power off VM: {str(e)}")


def create_vm_snapshot(si, vm_name: str, snapshot_name: str) -> str:
    """
    Creates a snapshot of the specified virtual machine (VM).

    Args:
        si: The ServiceInstance object representing the connection to vCenter.
        vm_name: The name of the VM to snapshot.
        snapshot_name: The name of the snapshot to be created.

    Returns:
        str: A message indicating the snapshot was created successfully.

    Raises:
        Exception: If there is an issue creating the snapshot.
    """

    try:
        vm = find_vm_by_name(si, vm_name)
        task = vm.CreateSnapshot(snapshot_name, memory=True, quiesce=False)
        task_info = task.info.state

        return f"Snapshot '{snapshot_name}' for VM '{vm_name}' created successfully. Task state: {task_info}"

    except Exception as e:
        raise Exception(f"Failed to create snapshot: {str(e)}")


def revert_vm_to_snapshot(si, vm_name: str, snapshot_name: str) -> str:
    """
    Reverts the specified virtual machine (VM) to a given snapshot.

    Args:
        si: The ServiceInstance object representing the connection to vCenter.
        vm_name: The name of the VM to revert.
        snapshot_name: The name of the snapshot to revert to.

    Returns:
        str: A message indicating that the VM was reverted to the snapshot.

    Raises:
        Exception: If there is an issue reverting to the snapshot.
    """

    try:
        vm = find_vm_by_name(si, vm_name)
        snapshots = vm.snapshot.rootSnapshotList

        for snapshot in snapshots:
            if snapshot.name == snapshot_name:
                task = snapshot.snapshot.RevertToSnapshot_Task()
                task_info = task.info.state
                return f"VM '{vm_name}' reverted to snapshot '{snapshot_name}'. Task state: {task_info}"

        raise Exception(f"Snapshot '{snapshot_name}' not found for VM '{vm_name}'.")

    except Exception as e:
        raise Exception(f"Failed to revert to snapshot: {str(e)}")


def list_datastores(si) -> str:
    """
    Retrieves a list of all datastores in the vSphere environment.

    Args:
        si: The ServiceInstance object representing the connection to vCenter.

    Returns:
        str: A list of datastore names and their capacity and free space.

    Raises:
        Exception: If there is an issue retrieving the datastores.
    """

    try:
        content = si.RetrieveContent()
        datastores_info = []

        for datacenter in content.rootFolder.childEntity:
            for datastore in datacenter.datastore:
                capacity = datastore.summary.capacity
                free_space = datastore.summary.freeSpace
                datastores_info.append(
                    f"{datastore.name}: Capacity - {capacity} bytes, Free Space - {free_space} bytes"
                )

        return f"Datastores: {', '.join(datastores_info)}"

    except Exception as e:
        raise Exception(f"Failed to retrieve datastores: {str(e)}")


def migrate_vm(si, vm_name: str, target_host: str) -> str:
    """
    Migrates the specified virtual machine (VM) to a new host.

    Args:
        si: The ServiceInstance object representing the connection to vCenter.
        vm_name: The name of the VM to migrate.
        target_host: The name of the target host for migration.

    Returns:
        str: A message indicating that the VM migration was successful.

    Raises:
        Exception: If there is an issue migrating the VM.
    """

    try:
        vm = find_vm_by_name(si, vm_name)
        content = si.RetrieveContent()
        target_host_obj = None

        # Find the target host object
        for datacenter in content.rootFolder.childEntity:
            for host in datacenter.hostFolder.childEntity:
                if host.name == target_host:
                    target_host_obj = host

        if not target_host_obj:
            raise Exception(f"Target host '{target_host}' not found.")

        task = vm.MigrateVM_Task(host=target_host_obj)
        task_info = task.info.state

        return (
            f"VM '{vm_name}' migrated to host '{target_host}'. Task state: {task_info}"
        )

    except Exception as e:
        raise Exception(f"Failed to migrate VM: {str(e)}")


def get_vm_network_details(si, vm_name: str) -> str:
    """
    Retrieves the network details for the specified virtual machine (VM).

    Args:
        si: The ServiceInstance object representing the connection to vCenter.
        vm_name: The name of the VM to retrieve network details for.

    Returns:
        str: The network configuration details of the VM.

    Raises:
        Exception: If there is an issue retrieving the network details.
    """

    try:
        vm = find_vm_by_name(si, vm_name)
        network_info = []

        for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualEthernetCard):
                network_info.append(
                    f"Network: {device.deviceInfo.summary}, MAC Address: {device.macAddress}"
                )

        return f"VM '{vm_name}' Network Details: {', '.join(network_info)}"

    except Exception as e:
        raise Exception(f"Failed to retrieve network details: {str(e)}")


def change_vm_network(si, vm_name: str, new_network: str) -> str:
    """
    Changes the network configuration for the specified virtual machine (VM).

    Args:
        si: The ServiceInstance object representing the connection to vCenter.
        vm_name: The name of the VM to change the network for.
        new_network: The name of the new network to connect to.

    Returns:
        str: A message indicating that the network was changed successfully.

    Raises:
        Exception: If there is an issue changing the network configuration.
    """

    try:
        vm = find_vm_by_name(si, vm_name)

        for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualEthernetCard):
                device.backing.network = new_network
                task = vm.ReconfigVM_Task()
                task_info = task.info.state
                return f"VM '{vm_name}' network changed to '{new_network}'. Task state: {task_info}"

        raise Exception(f"Failed to change network for VM '{vm_name}'.")

    except Exception as e:
        raise Exception(f"Failed to change VM network: {str(e)}")


def get_vm_storage_details(si, vm_name: str) -> str:
    """
    Retrieves the storage details for the specified virtual machine (VM).

    Args:
        si: The ServiceInstance object representing the connection to vCenter.
        vm_name: The name of the VM to retrieve storage details for.

    Returns:
        str: The storage configuration details of the VM.

    Raises:
        Exception: If there is an issue retrieving the storage details.
    """

    try:
        vm = find_vm_by_name(si, vm_name)
        storage_info = []

        for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualDisk):
                storage_info.append(
                    f"Disk: {device.deviceInfo.label}, Capacity: {device.capacityInKB} KB"
                )

        return f"VM '{vm_name}' Storage Details: {', '.join(storage_info)}"

    except Exception as e:
        raise Exception(f"Failed to retrieve storage details: {str(e)}")


def change_vm_storage(si, vm_name: str, new_datastore: str) -> str:
    """
    Changes the storage configuration for the specified virtual machine (VM).

    Args:
        si: The ServiceInstance object representing the connection to vCenter.
        vm_name: The name of the VM to change the storage for.
        new_datastore: The name of the new datastore to move the VM to.

    Returns:
        str: A message indicating that the storage was changed successfully.

    Raises:
        Exception: If there is an issue changing the storage configuration.
    """

    try:
        vm = find_vm_by_name(si, vm_name)
        content = si.RetrieveContent()
        datastore_obj = None

        # Find the datastore object
        for datacenter in content.rootFolder.childEntity:
            for datastore in datacenter.datastore:
                if datastore.name == new_datastore:
                    datastore_obj = datastore

        if not datastore_obj:
            raise Exception(f"Datastore '{new_datastore}' not found.")

        task = vm.MigrateVM_Task(pool=None, datastore=datastore_obj)
        task_info = task.info.state

        return f"VM '{vm_name}' moved to datastore '{new_datastore}'. Task state: {task_info}"

    except Exception as e:
        raise Exception(f"Failed to change VM storage: {str(e)}")


def validate_vm_compatibility(si, vm_name: str) -> str:
    """
    Validates the compatibility of the specified virtual machine (VM) with the target environment.

    Args:
        si: The ServiceInstance object representing the connection to vCenter.
        vm_name: The name of the VM to validate.

    Returns:
        str: A message indicating the compatibility status of the VM.

    Raises:
        Exception: If there is an issue validating the VM compatibility.
    """

    try:
        vm = find_vm_by_name(si, vm_name)

        # Simplified compatibility check; in reality, this would check against target environment specs
        if vm.config.guestFullName in ["Linux", "Windows"]:
            return f"VM '{vm_name}' is compatible with the target environment."

        return f"VM '{vm_name}' is not compatible with the target environment."

    except Exception as e:
        raise Exception(f"Failed to validate VM compatibility: {str(e)}")


def delete_vm_snapshot(si, vm_name: str, snapshot_name: str) -> str:
    """
    Deletes a snapshot of the specified virtual machine (VM).

    Args:
        si: The ServiceInstance object representing the connection to vCenter.
        vm_name: The name of the VM.
        snapshot_name: The name of the snapshot to delete.

    Returns:
        str: A message indicating the snapshot was deleted successfully.

    Raises:
        Exception: If there is an issue deleting the snapshot.
    """

    try:
        vm = find_vm_by_name(si, vm_name)
        snapshots = vm.snapshot.rootSnapshotList

        for snapshot in snapshots:
            if snapshot.name == snapshot_name:
                task = snapshot.snapshot.RemoveSnapshot_Task()
                task_info = task.info.state
                return f"Snapshot '{snapshot_name}' deleted for VM '{vm_name}'. Task state: {task_info}"

        raise Exception(f"Snapshot '{snapshot_name}' not found for VM '{vm_name}'.")

    except Exception as e:
        raise Exception(f"Failed to delete snapshot: {str(e)}")
