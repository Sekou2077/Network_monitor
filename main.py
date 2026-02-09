# Author: Sekou Traore
# Network monitoring script
# Make a minimum working version and incrementally improve
# Filter for specific socket connections based on criteria
# Make output more user-friendly(change AF_INET to IPv4, etc.)
# Start styling the interface with rich
# Start sniffing packets

import os
import socket
import time

# interesting library that provides system and network information(psutil)
import psutil
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import track
from rich.theme import Theme
from scapy.all import sniff

# Custom theming
custom_theme = Theme(
    {
        "general": "dim cyan",
        "tcp": "orange_red1",
        "udp": "deep_pink4",
        "ipv4": "bold green",
        "ipv6": "bold blue",
    }
)

# Initialize rich console for better output formatting
console = Console(theme=custom_theme)

# Load environment variables from .env file
load_dotenv()

# Returns system-wide network I/O statistics as a named tuple(pernic=False condenses stats for all network interfaces)
network_stats = psutil.net_io_counters(pernic=False, nowrap=True)
# Get a list of all current socket connections(Only Ipv4 and IPv6 connections)
socket_connections = psutil.net_connections(kind="inet")
# Get network interface card information as a dictionary whose keys are NIC names and values are a named tuple
network_interfaces = psutil.net_if_stats()

console.print("Welcome to my network monitoring script", style="general")
time.sleep(1)
# Simulate gathering data with a progress bar
for i in track(
    range(5),
    description="Gathering system wide network statistics...",
    style="green",
):
    time.sleep(2)

# Display network statistics in easier formatting
print(
    f" System wide network stats: bytes sent = {network_stats.bytes_sent}, bytes received = {network_stats.bytes_recv},"
    f"pac"
    f"kets sent = {network_stats.packets_sent}, packets received = {network_stats.packets_recv}, total receiving errors"
    f" = {network_stats.errin}, total sending errors = {network_stats.errout}, total dropped packets"
    f" = {network_stats.dropin + network_stats.dropout}"
)

# Simulate processing socket connections with a progress bar
for _i in track(
    range(3), description="Processing socket connections...", style="yellow"
):
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
        # Neat tricks for styling output with markup(rich)
        family_name = (
            "[ipv4]IPv4[/ipv4]"
            if connection.family == socket.AF_INET
            else "[ipv6]IPv6[/ipv6]"
        )
        type_name = (
            "[tcp]TCP[/tcp]"
            if connection.type == socket.SOCK_STREAM
            else "[udp]UDP[/udp]"
        )

        console.print(
            f"Socket connection: family={family_name}, type={type_name}"
            f",status={connection.status},"
            f" local address={connection.laddr}"
        )

# Display network interface information
# filter out loopback(self) and LANs to show more live information
for _i in track(range(3), description="Processing network interfaces...", style="red"):
    time.sleep(3)
for interface_name, interface_info in network_interfaces.items():
    is_up = "up" if interface_info.isup else "down"
    if interface_name.lower().startswith(
        "loopback"
    ) or interface_name.lower().startswith("local"):
        continue
    print(
        f"Interface: {interface_name}, status={is_up}, speed={interface_info.speed}MB, "
        f"Maximum transmission Unit={interface_info.mtu} bytes"
    )


# Function to process sniffed packets and display relevant information(scapy only captures silently)
def process_packet(packet):
    if packet.haslayer("IP"):
        ip_layer = packet["IP"]
        src_ip = ip_layer.src
        dst_ip = ip_layer.dst
        protocol = ip_layer.proto
        # Map protocol numbers to names for better readability
        if protocol == 6:
            protocol = "TCP"
        elif protocol == 17:
            protocol = "UDP"
        console.print(
            f"Packet: [general]Source IP:[/general] {src_ip} ->  [general]Destination IP:[/general] {dst_ip}, "
            f"[general]Protocol:[/general] {protocol}"
        )


# Fetch the IP address
ip_address = os.getenv("IP_ADDRESS")
print("Capturing traffic involving IP address(Ctrl+C to stop):", ip_address)
# Start sniffing packets that involve the specified IP address

# Sniffing packets using processing function and make sure non-promiscuous mode is used to avoid capturing all traffic
# on the network and only capture traffic relevant to the host
try:
    sniff(
        filter=f"host {ip_address}",
        prn=process_packet,
        store=False,
        promisc=False,
    )
finally:
    console.print("Sniffing session stopped by user.", style="general")
