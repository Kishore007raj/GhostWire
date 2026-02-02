import time  # Import time module for sleep functionality.
from agent.capture.connections import get_outbound_connections  # Import function to get outbound connections.
from agent.process.mapper import enrich_connections  # Import function to enrich connections with process info.
from agent.traffic.bandwidth import BandwidthTracker  # Import BandwidthTracker class for network monitoring.

def run_agent():
    """
    Main function to run the network monitoring agent.
    Continuously monitors outbound connections, enriches them with process details,
    tracks bandwidth, and distributes bandwidth data per process.
    """
    bw = BandwidthTracker()  # Initialize the bandwidth tracker.

    while True:  # Infinite loop to monitor continuously.
        connections = get_outbound_connections()  # Get the list of outbound connections.
        enriched = enrich_connections(connections)  # Enrich connections with process details.

        bw_sample = bw.sample()  # Sample current bandwidth data.
        if bw_sample is None:  # If no sample yet (first run), skip and wait.
            time.sleep(2)
            continue

        # Build PID → list of connections mapping.
        pid_map = {}
        for item in enriched:
            pid_map.setdefault(item["pid"], []).append(item)  # Group connections by PID.

        pid_count = len(pid_map)  # Get the number of unique PIDs.

        if pid_count == 0:  # If no active PIDs, skip and wait.
            time.sleep(2)
            continue

        # Split bandwidth per PID (NOT per connection).
        per_pid_sent = bw_sample["bytes_sent"] // pid_count  # Calculate sent bytes per PID.
        per_pid_recv = bw_sample["bytes_recv"] // pid_count  # Calculate received bytes per PID.

        for pid, items in pid_map.items():  # Iterate over each PID and its connections.
            for item in items:  # For each connection under this PID.
                item["bytes_sent"] = per_pid_sent  # Assign sent bytes.
                item["bytes_recv"] = per_pid_recv  # Assign received bytes.
                item["timestamp"] = bw_sample["timestamp"]  # Assign timestamp.

                print(item)  # Print the enriched connection with bandwidth data.

        time.sleep(2)  # Wait 2 seconds before the next iteration.

if __name__ == "__main__":
    run_agent()  # Run the agent when the script is executed directly.
