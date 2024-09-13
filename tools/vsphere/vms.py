import os
from dotenv import load_dotenv
from langchain.tools import tool
from typing import Union, List, Dict
from utils.vsphere.vsphere_utils import (
    get_all_vms,
    connect_to_vsphere,
    disconnect_from_vsphere,
    get_vm_details,
    get_vm_by_name,
)


load_dotenv()

vsphere_config = {
    "host": os.getenv("VSPHERE_HOST"),
    "username": os.getenv("VSPHERE_USERNAME"),
    "password": os.getenv("VSPHERE_PASSWORD"),
}

@tool(parse_docstring=True)
def list_vms() -> Union[List[str], str]:
    """
    A wrapper around a vSphere utility for listing all available virtual machines (VMs). Useful for retrieving a list of VMs from the connected vSphere environment.

    Returns:
        vms: A list of VM names or an error message if the operation fails.
    """
    si = None
    try:
        # Connect to vSphere
        si, content = connect_to_vsphere(
            host=vsphere_config["host"],
            user=vsphere_config["username"],
            pwd=vsphere_config["password"],
        )

        vms, vm_names = get_all_vms(si, content)
        return vm_names

    except Exception as e:
        return f"Failed to list vms. {str(e)}"

    finally:
        if si:
            disconnect_from_vsphere(si)


@tool(parse_docstring=True)
def retrieve_vm_details(vm_name: str) -> Union[Dict[str, Union[str, int, list]], str]:
    """
    A wrapper around a vSphere utility for extracting detailed information about a specific virtual machine (VM). Useful for retrieving the VM's operating system, resource allocations, and network configurations based on the provided VM name.

    Args:
        vm_name: The name of the virtual machine to retrieve details for.

    Returns:
        vm_details: A dictionary containing VM details or an error message if the operation fails or the VM is not found.
    """
    si = None
    try:
        # Connect to vSphere
        si, content = connect_to_vsphere(
            host=vsphere_config["host"],
            user=vsphere_config["username"],
            pwd=vsphere_config["password"],
        )

        # Find the VM by name
        vm = get_vm_by_name(content, vm_name)

        if not vm:
            return f"VM '{vm_name}' not found."

        # Get detailed information about the found VM
        vm_details = get_vm_details(vm)
        return vm_details

    except Exception as e:
        return f"Failed to retrieve details for VM '{vm_name}': {str(e)}"

    finally:
        if si:
            disconnect_from_vsphere(si)
