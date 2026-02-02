import psutil  # Import psutil for network I/O counters.
import time  # Import time for timestamp handling.

class BandwidthTracker:
    """
    A class to track network bandwidth by sampling bytes sent and received over time intervals.

    This tracker calculates the difference in network traffic between consecutive samples,
    providing deltas for bytes sent, received, and the time interval.
    """

    def __init__(self):
        """
        Initialize the BandwidthTracker with previous values set to None.
        """
        self.prev_sent = None  # Store the previous bytes sent.
        self.prev_recv = None  # Store the previous bytes received.
        self.prev_time = None  # Store the previous timestamp.

    def sample(self):
        """
        Sample the current network I/O counters and calculate bandwidth deltas.

        Returns:
            dict or None: A dictionary with 'bytes_sent', 'bytes_recv', 'interval', and 'timestamp'
                          if deltas can be calculated; None on the first sample.
        """
        counters = psutil.net_io_counters(pernic=False)  # Get overall network I/O counters.

        now = time.time()  # Get the current timestamp.
        sent = counters.bytes_sent  # Get total bytes sent.
        recv = counters.bytes_recv  # Get total bytes received.

        # On the first run, initialize previous values and return None (no delta yet).
        if self.prev_sent is None:
            self.prev_sent = sent
            self.prev_recv = recv
            self.prev_time = now
            return None

        # Calculate deltas: difference in bytes sent, received, and time.
        delta_sent = sent - self.prev_sent
        delta_recv = recv - self.prev_recv
        delta_time = now - self.prev_time

         # Guard against counter reset / weird OS behavior
        delta_sent = max(0, delta_sent)
        delta_recv = max(0, delta_recv)

        # Update previous values for the next sample.
        self.prev_sent = sent
        self.prev_recv = recv
        self.prev_time = now

        # Return the bandwidth data as a dictionary.
        return {
            "bytes_sent": delta_sent,  # Bytes sent in this interval.
            "bytes_recv": delta_recv,  # Bytes received in this interval.
            "interval": delta_time,    # Time interval in seconds.
            "timestamp": now           # Current timestamp.
        }
