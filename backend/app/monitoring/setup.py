import psutil
from prometheus_client import REGISTRY, Metric
import platform

class WindowsProcessCollector:
    def collect(self):
        #gets process information
        process = psutil.Process()
        
        # Custom Memory metric (RSS)
        memory_metric = Metric(
            "process_resident_memory_bytes", 
            "Resident memory size in bytes (Windows)", 
            "gauge"
        )
        #adds a sample of the current process information to the TS database
        memory_metric.add_sample(
            "process_resident_memory_bytes", 
            value=process.memory_info().rss, 
            labels={}
        )
        #saves the metric in an iterator
        yield memory_metric

        # Custom CPU metric
        cpu_metric = Metric(
            "process_cpu_percent", 
            "Process CPU usage percent (Windows)", 
            "gauge"
        )
        #adds a sample of the current CPU utilization metric to the TS database
        cpu_metric.add_sample(
            "process_cpu_percent", 
            value=process.cpu_percent(), 
            labels={}
        )
        yield cpu_metric

# Register it ONCE on app startup
def setup_monitoring():
    if platform.system().lower() == "windows":
        try:
            REGISTRY.register(WindowsProcessCollector())
        except:
            pass