import psutil  # Import the psutil library to access system and network information.
import socket  # Import the socket library for network-related operations.

def get_outbound_connections():  # Define a function to get outbound network connections.
    result = []  # Initialize an empty list to store connection details.
    for conn in psutil.net_connections(kind='inet'):  # Iterate over all internet connections.

        if conn.pid is None:  # Check if the connection has a process ID.
            continue  # Skip to the next connection if no PID is found.

        if not conn.laddr or not conn.raddr:  # Ensure both local and remote addresses exist.
            continue  # Skip to the next connection if either address is missing.

        if conn.status != psutil.CONN_ESTABLISHED:  # Check if the connection is established.
            continue  # Skip to the next connection if it is not established.

        laddr = conn.laddr  # Get the local address of the connection.
        raddr = conn.raddr  # Get the remote address of the connection.

        protocol = 'tcp' if conn.type == socket.SOCK_STREAM else 'udp'  # Determine the protocol type (TCP or UDP).

        result.append({  # Append the connection details to the result list.
            'pid': conn.pid,  # Add the process ID.
            'protocol': protocol,  # Add the protocol type.
            'local_ip': laddr.ip,  # Add the local IP.
            'local_port': laddr.port,  # Add the local port.
            'remote_ip': raddr.ip,  # Add the remote IP.
            'remote_port': raddr.port,  # Add the remote port.
            'status': conn.status  # Add the connection status.
        })

    return result  # Return the list of active connections.