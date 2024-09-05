output_vm_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},  # Name of the virtual machine.
        "operating_system": {"type": "string"},  # Operating system of the VM.
        "cpu": {"type": "integer", "minimum": 1},  # Number of CPUs allocated.
        "memory_mb": {
            "type": "integer",  # Amount of memory allocated in MB.
            "minimum": 1,
        },
        "disks": {
            "type": "array",  # List of disks attached to the VM.
            "items": {
                "type": "object",
                "properties": {
                    "label": {"type": "string"},  # Disk label (e.g., "Hard disk 1").
                    "capacity_gb": {
                        "type": "number",  # Disk capacity in GB.
                        "minimum": 0,
                    },
                },
                "required": [
                    "label",
                    "capacity_gb",
                ],  # Both label and capacity are required.
            },
        },
        "networks": {
            "type": "array",  # List of network interfaces attached to the VM.
            "items": {"type": "string"},  # Network interface names as strings.
            "default": [],  # Default to an empty array if no networks are provided.
        },
        "power_state": {
            "type": "string",  # Power state of the VM.
            "enum": ["poweredOff", "poweredOn", "suspended"],  # Allowed power states.
        },
        "connection_state": {
            "type": "string",  # Connection state of the VM.
            "enum": [
                "connected",
                "disconnected",
                "notResponding",
            ],  # Allowed connection states.
        },
        "overall_status": {
            "type": "string",  # Overall health status of the VM.
            "enum": ["green", "yellow", "red"],  # Allowed statuses.
        },
    },
    "required": [
        "name",  # Name is required.
        "operating_system",  # Operating system is required.
        "cpu",  # CPU allocation is required.
        "memory_mb",  # Memory allocation is required.
        "disks",  # Disks information is required.
        "networks",  # Networks information is required.
        "power_state",  # Power state is required.
        "connection_state",  # Connection state is required.
        "overall_status",  # Overall status is required.
    ],
}
