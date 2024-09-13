import os
from dotenv import load_dotenv
from typing import List, Dict, Union
from langchain.tools import tool
from services.openshift_service import OpenShiftService

load_dotenv()

openshift_config = {
    "api_url": os.getenv("OPENSHIFT_API_URL"),
    "console_url": os.getenv("OPENSHIFT_CONSOLE_URL"),
    "token": os.getenv("OPENSHIFT_TOKEN"),
    "inventory_route": os.getenv("OPENSHIFT_INVENTORY_ROUTE"),
}

openshift_service = OpenShiftService(openshift_config=openshift_config)


@tool(parse_docstring=True)
def create_migration_plan_tool(
    vm_names: List[str],
    name: str,
    source: str = "vmware",
) -> Union[Dict, str]:
    """
    A tool to create a migration plan for moving virtual machines (VMs) using the forklift.konveyor.io API. This tool only requires VM names, and the corresponding IDs are fetched automatically.

    Args:
        vm_names: A list of VM names to migrate. This arg is mandatory.
        name: The name of the migration plan. This arg is mandatory.
        source: The source provider. Default is 'vmware'.

    Returns:
        dict: The created migration plan if successful.
        str: An error message if the operation fails.
    """
    try:
        # Create an OpenShiftService instance
        OpenShiftService(openshift_config=openshift_config)
        print("\n1/8 Connected to Openshift...\n")

        # Automatically lookup the provider UUID based on the source provider name
        vmware_provider_uuid = openshift_service.lookup_provider_uuid_by_name(
            provider_name="vmware", provider_type="vsphere"
        )
        if isinstance(vmware_provider_uuid, str) and "Error" in vmware_provider_uuid:
            return vmware_provider_uuid  # Return the error if we encountered one

        if vmware_provider_uuid is None:
            return f"Provider '{source}' not found."
        print(f"\n2/8 Now I have the source provider ID {vmware_provider_uuid}...\n")

        openshift_provider_uuid = openshift_service.lookup_provider_uuid_by_name(
            provider_name="host", provider_type="openshift"
        )
        if (
            isinstance(openshift_provider_uuid, str)
            and "Error" in openshift_provider_uuid
        ):
            return openshift_provider_uuid  # Return the error if we encountered one

        if openshift_provider_uuid is None:
            return f"Provider OpenShift not found."

        print(f"\n3/8 Now I have the host provider ID {openshift_provider_uuid}...\n")

        network_id = openshift_service.get_network_id_by_name(
            provider_uuid=vmware_provider_uuid
        )
        print(f"\n4/8 Now I have the source network ID {network_id}...\n")

        # If no VM names are provided, use a default VM
        if vm_names is None:
            return f"Failed to create migration plan: No VM was provided!"

        # Fetch VM IDs for the given VM names
        vms = []
        for vm_name in vm_names:
            vm_id = openshift_service.lookup_vm_id_by_name(
                vmware_provider_uuid, vm_name
            )

            # Assuming error messages are distinct, e.g., returned as dicts or special error codes
            if isinstance(vm_id, dict) and "error" in vm_id:
                return vm_id["error"]  # This handles the error case

            # Check if VM was found
            if vm_id:
                vms.append({"id": vm_id, "name": vm_name})
            else:
                return f"VM '{vm_name}' not found."

        print(f"\n5/8 Now I have all the VM Names and all the VM IDs {vms}...\n")

        datastore_id = openshift_service.get_datastore_id_by_vm_id(
            provider_uuid=vmware_provider_uuid, vm_id=vms[0]["id"]
        )
        print(f"\n5/8 Now I have the source datastore ID {datastore_id}...\n")

        network_map, nm_uid, network_map_name = openshift_service.create_network_map(
            source_provider_uid=vmware_provider_uuid,
            destination_provider_uid=openshift_provider_uuid,
            source_network_id=network_id,
        )

        storage_map, sm_uid, storage_map_name = openshift_service.create_storage_map(
            source_provider_uid=vmware_provider_uuid,
            destination_provider_uid=openshift_provider_uuid,
            source_datastore_id=datastore_id,
        )

        print(f"\n7/8 Now I have the Storage and Network maps {vms}...\n")

        # Call the create_migration_plan method with the gathered information
        result = openshift_service.create_migration_plan(
            network_map_uid=nm_uid,
            network_map_name=network_map_name,
            storage_map_uid=sm_uid,
            storage_map_name=storage_map_name,
            name=name,
            source=source,
            vms=vms,
        )

        print(f"\n8/8 Migration plan RESPONSE - {result}...\n")
        return result

    except Exception as e:
        return f"Failed to create migration plan: {str(e)}"


@tool(parse_docstring=True)
def start_migration_plan_tool(
    plan_name: str, namespace: str = "openshift-mtv"
) -> Union[Dict, str]:
    """
    A tool to start a migration for a given migration plan by its name.

    Args:
        plan_name: The name of the migration plan. The value should consist of lower case alphanumeric characters, '-' or '.', and must start and end with an alphanumeric character (e.g. 'example.com', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*').
        namespace: The namespace where the migration plan is located. Default is 'openshift-mtv'.


    Returns:
        dict: The migration start response if successful.
        str: An error message if the operation fails.
    """
    try:
        # Create an OpenShiftService instance
        OpenShiftService(openshift_config=openshift_config)
        print("\n1/4 Connected to Openshift...\n")

        # Retrieve the full migration plan object by its name
        migration_plan = openshift_service.get_migration_plan_by_name(
            plan_name=plan_name, namespace=namespace
        )

        if isinstance(migration_plan, str) and "Error" in migration_plan:
            return migration_plan  # Return the error if we encountered one

        if migration_plan is None:
            return f"Migration plan '{plan_name}' not found."

        # Retrieve the UID of the migration plan
        plan_uid = migration_plan["metadata"]["uid"]
        print(f"\n2/4 Retrieved migration plan UID: {plan_uid}...\n")

        # Check the status conditions to verify if the plan is ready
        ready_status = False
        conditions = migration_plan.get("status", {}).get("conditions", [])
        for condition in conditions:
            if condition.get("type") == "Ready" and condition.get("status") == "True":
                ready_status = True
                break

        if not ready_status:
            return f"Migration plan '{plan_name}' is not ready."

        print(f"\n3/4 Migration plan is ready. Starting migration...\n")

        # Start the migration using the retrieved plan UID
        result = openshift_service.start_migration(
            plan_name=plan_name, plan_uid=plan_uid, namespace=namespace
        )

        print(f"\n4/4 Migration started: {result}...\n")
        return result

    except Exception as e:
        return f"Failed to start migration: {str(e)}"
