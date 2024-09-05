output_vms_schema = {
    "type": "object",
    "properties": {
        "vms": {
            "type": "string",  # The 'vms' field is a string that contains a list-like structure.
            "pattern": r"^\[.*\]$"  # This regex pattern ensures that the string starts with '[' and ends with ']'.
        }
    },
    "required": ["vms"]  # The 'vms' field is required.
}
