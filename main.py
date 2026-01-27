# Author: Sekou Traore
# Network monitoring script
# Make a minimum working version and incrementally improve


# interesting library that provides system and network information
import psutil
import time


# Returns system-wide network I/O statistics as a named tuple(pernic=False lists all interfaces and allows me to
# access individual interface stats since the returned object remains a named tuple)
network_stats = psutil.net_io_counters(pernic=False, nowrap=True)
# Get a list of all current socket connections(Only Ipv4 and IPv6 connections)
socket_connections = psutil.net_connections(kind="inet")

print("Welcome to my network monitoring script")
time.sleep(1)
print("Gathering network statistics...")
time.sleep(3)
# Display network statistics in easier formatting
print(
    f"network stats: bytes sent = {network_stats.bytes_sent}, bytes received = {network_stats.bytes_recv}, pac"
    f"kets sent = {network_stats.packets_sent}, packets received = {network_stats.packets_recv}, total receiving errors"
    f" = {network_stats.errin}, total sending errors = {network_stats.errout}, total dropped packets"
    f" = {network_stats.dropin + network_stats.dropout}"
)

# Display socket connections based on some criteria:
# Only IPV4(AF_INET) and IPV6(AF_INET6) address family connections
# Only TCP(SOCK_STREAM) and UDP(SOCK_DGRAM) socket types
# State is established connections(the connection is open and data can be sent and received)


for connection in socket_connections:
    if connection.family in (psutil.AF_INET, psutil.AF_INET6) and connection.type in (
        psutil.SOCK_STREAM,
        psutil.SOCK_DGRAM,
    ) and connection.status == psutil.CONN_ESTABLISHED:

print(f"Socket connections: {socket_connections}")
