# Author: Sekou Traore
# Network monitoring script
# Make a minimum working version and incrementally improve


# interesting library that provides system and network information
import psutil
import time


# Returns system-wide network I/O statistics as a named tuple(pernic=True for per network interface)
network_stats = psutil.net_io_counters(pernic=False, nowrap=True)

print("Welcome to my network monitoring script")
time.sleep(1)
print("Gathering network statistics...")
time.sleep(3)
print(network_stats)
