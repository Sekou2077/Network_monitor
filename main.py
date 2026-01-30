# Author: Sekou Traore
# Network monitoring script
# Make a minimum working version and incrementally improve
# Filter for specific socket connections based on criteria
# Make output more user-friendly(change AF_INET to IPv4, etc.)

# interesting library that provides system and network information
import psutil
import time
import socket

# Returns system-wide network I/O statistics as a named tuple(pernic=False condenses stats for all network interfaces)
network_stats = psutil.net_io_counters(pernic=False, nowrap=True)
# Get a list of all current socket connections(Only Ipv4 and IPv6 connections)
socket_connections = psutil.net_connections(kind="inet")
# Get network interface card information as a dictionary whose keys are NIC names and values are a named tuple
network_interfaces = psutil.net_if_stats()

print("Welcome to my network monitoring script")
time.sleep(1)
print("Gathering network statistics...")
time.sleep(3)
# Display network statistics in easier formatting
print(
    f" system wide network stats: bytes sent = {network_stats.bytes_sent}, bytes received = {network_stats.bytes_recv},"
    f"pac"
    f"kets sent = {network_stats.packets_sent}, packets received = {network_stats.packets_recv}, total receiving errors"
    f" = {network_stats.errin}, total sending errors = {network_stats.errout}, total dropped packets"
    f" = {network_stats.dropin + network_stats.dropout}"
)

print("Gathering socket connection information...")
time.sleep(3)
# Display socket connections based on some criteria:
# Only IPV4(AF_INET) and IPV6(AF_INET6) address family connections
# Only TCP(SOCK_STREAM) and UDP(SOCK_DGRAM) socket types
# State is established connections(the connection is open and data can be sent and received)
# The socket library is needed to interpret the address family and socket type constants
# UDP connections have a status of NONE since it is connectionless
for connection in socket_connections:
    if (
        connection.family in (socket.AF_INET, socket.AF_INET6)
        and connection.type
        in (
            socket.SOCK_STREAM,
            socket.SOCK_DGRAM,
        )
        and (
            connection.status == psutil.CONN_ESTABLISHED
            or connection.status == psutil.CONN_NONE
        )
    ):
        family_name = "IPv4" if connection.family == socket.AF_INET else "IPv6"
        type_name = "TCP" if connection.type == socket.SOCK_STREAM else "UDP"
        print(
            f"Socket connection: family={family_name}, type={type_name},status={connection.status},"
            f" local address={connection.laddr}"
        )

# Display network interface information
print("Gathering network interface information...")
time.sleep(3)
for interface_name, interface_info in network_interfaces.items():
    is_up = "up" if interface_info.isup else "down"
    print(
        f"Interface: {interface_name}, status={is_up}, speed={interface_info.speed}Mbps, "
        f"MTU={interface_info.mtu}"
    )
