
import psutil

network_stats = psutil.net_io_counters(pernic=False, nowrap=True)
print(network_stats)
