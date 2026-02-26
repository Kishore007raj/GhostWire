import psutil  # Import psutil library for system and process utilities.

def enrich_connections(connections):
    """
    Enrich the list of network connections with additional process information.

    Args:
        connections (list): A list of dictionaries representing network connections.
                            Each dict should contain keys like 'pid', 'protocol', etc.

    Returns:
        list: A list of enriched connection dictionaries with added process details.
    """
    enriched = []  # Initialize a list to hold the enriched connection data.

    for conn in connections:  # Iterate over each connection in the input list.
        pid = conn["pid"]  # Extract the process ID from the connection dictionary.

        try:
            # Attempt to get the process object using the PID.
            proc = psutil.Process(pid)

            # Append enriched connection data with process information.
            enriched.append({
                **conn,  # Include all original connection data.
                "process_name": proc.name(),  # Add the process name.
                "exe": proc.exe(),  # Add the executable path.
            })

        except Exception:
            # Handle cases where the process no longer exists or access is denied.
            enriched.append({
                **conn,  # Include all original connection data.
                "process_name": "unknown",  # Set process name to unknown.
                "exe": None,  # No executable path available.
            })

    return enriched  # Return the list of enriched connections.
