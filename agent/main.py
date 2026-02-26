import time  # Import time module for sleep functionality.
from agent.capture.connections import get_outbound_connections  # Import function to get outbound connections.
from agent.process.mapper import enrich_connections  # Import function to enrich connections with process info.
from agent.traffic.bandwidth import BandwidthTracker  # Import BandwidthTracker class for network monitoring.
from agent.store.db import GhostwireDB  # Import GhostwireDB class for database operations.
from agent.detect.engine import run_detection  # Import function to run detection rules.

def run_agent():
    """
    Main function to run the network monitoring agent.
    Continuously monitors outbound connections, enriches them with process details,
    tracks bandwidth, and distributes bandwidth data per process.
    """
    bw = BandwidthTracker()  # Initialize the bandwidth tracker.
    db = GhostwireDB()  # Initialize the database.

    while True:  # Infinite loop to monitor continuously.
        try:
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
                # Insert bandwidth summary for this PID
                try:
                    process_name = items[0]["process_name"]
                    exe = items[0]["exe"]
                    db.insert_bandwidth_summary({
                        "timestamp": bw_sample["timestamp"],
                        "pid": pid,
                        "process_name": process_name,
                        "exe": exe,
                        "bytes_sent": per_pid_sent,
                        "bytes_recv": per_pid_recv,
                        "interval": bw_sample["interval"]
                    })
                except Exception as e:
                    print(f"Error inserting bandwidth summary for PID {pid}: {e}")
                    continue

                for item in items:  # For each connection under this PID.
                    item["bytes_sent"] = per_pid_sent  # Assign sent bytes.
                    item["bytes_recv"] = per_pid_recv  # Assign received bytes.
                    item["timestamp"] = bw_sample["timestamp"]  # Assign timestamp.

                    alerts = run_detection(item)  # Run detection rules on this enriched connection.
                    for alert in alerts:  # If any alerts are generated, insert them into the database.
                        try:
                            print("Alert:", alert)
                            db.insert_alert(alert)
                        except Exception as e:
                            print(f"Error inserting alert: {e}")
                            continue

                    try:
                        db.insert_connection(item)  # Insert the enriched connection into the database.
                    except Exception as e:
                        print(f"Error inserting connection: {e}")
                        continue

                    print(item)  # Print the enriched connection with bandwidth data.

            try:
                db.commit()  # Commit all database changes.
            except Exception as e:
                print(f"Error committing transaction: {e}")
                db.rollback()  # Rollback on commit failure to prevent inconsistent state.
        
        except Exception as e:
            # Catch unexpected errors from data gathering phase.
            print(f"Unexpected error in iteration: {e}")
            try:
                db.rollback()
            except Exception as rollback_error:
                print(f"Error during rollback: {rollback_error}")

        time.sleep(2)  # Wait 2 seconds before the next iteration.

if __name__ == "__main__":
    run_agent()  # Run the agent when the script is executed directly.
