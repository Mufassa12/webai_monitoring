import os
import time
import psutil
import platform
import logging
import subprocess
import json
import re
from datetime import datetime
from flask import Flask, Response
from prometheus_client import Counter, Gauge, Histogram, generate_latest, REGISTRY, CONTENT_TYPE_LATEST

# Get user's home directory for log file
user_home = os.path.expanduser("~")
log_file = os.path.join(user_home, "webai_monitoring.log")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=log_file
)

logger = logging.getLogger('WebAI-Monitor')

# Initialize Flask
app = Flask(__name__)

# Define Prometheus metrics
CPU_USAGE = Gauge('webai_cpu_usage_percent', 'CPU usage in percent')
MEMORY_TOTAL = Gauge('webai_memory_total_bytes', 'Total memory in bytes')
MEMORY_AVAILABLE = Gauge('webai_memory_available_bytes', 'Available memory in bytes')
MEMORY_USED = Gauge('webai_memory_used_bytes', 'Used memory in bytes')
MEMORY_PERCENT = Gauge('webai_memory_usage_percent', 'Memory usage in percent')

DISK_TOTAL = Gauge('webai_disk_total_bytes', 'Total disk space in bytes')
DISK_USED = Gauge('webai_disk_used_bytes', 'Used disk space in bytes')
DISK_FREE = Gauge('webai_disk_free_bytes', 'Free disk space in bytes')
DISK_PERCENT = Gauge('webai_disk_usage_percent', 'Disk usage in percent')

# Add disk I/O metrics
DISK_READ_BYTES = Gauge('webai_disk_read_bytes_per_sec', 'Disk read bytes per second')
DISK_WRITE_BYTES = Gauge('webai_disk_write_bytes_per_sec', 'Disk write bytes per second')
DISK_READ_IOPS = Gauge('webai_disk_read_iops', 'Disk read operations per second')
DISK_WRITE_IOPS = Gauge('webai_disk_write_iops', 'Disk write operations per second')

NETWORK_BYTES_SENT = Gauge('webai_network_bytes_sent', 'Network bytes sent')
NETWORK_BYTES_RECV = Gauge('webai_network_bytes_recv', 'Network bytes received')
NETWORK_PACKETS_SENT = Gauge('webai_network_packets_sent', 'Network packets sent')
NETWORK_PACKETS_RECV = Gauge('webai_network_packets_recv', 'Network packets received')
NETWORK_BYTES_SENT_PER_SEC = Gauge('webai_net_sent_bytes_per_sec', 'Network bytes sent per second')
NETWORK_BYTES_RECV_PER_SEC = Gauge('webai_net_recv_bytes_per_sec', 'Network bytes received per second')

SYSTEM_UPTIME = Gauge('webai_system_uptime_seconds', 'System uptime in seconds')

# Add GPU metrics
GPU_USAGE = Gauge('webai_gpu_usage_percent', 'GPU usage in percent')
GPU_POWER = Gauge('webai_gpu_power_watts', 'GPU power usage in watts')

# Add NPU metrics (simulated for Apple Silicon)
NPU_USAGE = Gauge('webai_npu_usage_percent', 'NPU usage in percent (simulated)')
NPU_POWER = Gauge('webai_npu_power_watts', 'NPU power usage in watts (simulated)')

# Add CPU power metrics
CPU_POWER = Gauge('webai_cpu_power_watts', 'CPU power usage in watts')

class SystemMonitor:
    def __init__(self):
        self.system_info = {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'hostname': platform.node()
        }
        
        # Initialize disk IO counters
        self.prev_disk_io = psutil.disk_io_counters()
        self.prev_disk_time = time.time()
        
        # Initialize network counters
        self.prev_net_io = psutil.net_io_counters()
        self.prev_net_time = time.time()
        
        # Check if we're on Apple Silicon
        self.is_apple_silicon = self.system_info['architecture'] == 'arm64' and self.system_info['platform'] == 'Darwin'
        
        logger.info(f"System Monitor initialized on {self.system_info['hostname']}")
        logger.info(f"Apple Silicon: {self.is_apple_silicon}")
    
    def get_cpu_usage(self):
        """Return the CPU usage as a percentage."""
        return psutil.cpu_percent(interval=1)
    
    def get_memory_usage(self):
        """Return memory usage statistics."""
        memory = psutil.virtual_memory()
        return {
            'total': memory.total,
            'available': memory.available,
            'percent': memory.percent,
            'used': memory.used,
            'free': memory.free
        }
    
    def get_disk_usage(self):
        """Return disk usage statistics."""
        disk = psutil.disk_usage('/')
        return {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent
        }
    
    def get_disk_io(self):
        """Return disk I/O statistics."""
        current_disk_io = psutil.disk_io_counters()
        current_time = time.time()
        
        # Calculate time difference
        time_diff = current_time - self.prev_disk_time
        
        # Calculate rates
        read_bytes_per_sec = (current_disk_io.read_bytes - self.prev_disk_io.read_bytes) / time_diff
        write_bytes_per_sec = (current_disk_io.write_bytes - self.prev_disk_io.write_bytes) / time_diff
        read_count_per_sec = (current_disk_io.read_count - self.prev_disk_io.read_count) / time_diff
        write_count_per_sec = (current_disk_io.write_count - self.prev_disk_io.write_count) / time_diff
        
        # Update previous values
        self.prev_disk_io = current_disk_io
        self.prev_disk_time = current_time
        
        return {
            'read_bytes_per_sec': read_bytes_per_sec,
            'write_bytes_per_sec': write_bytes_per_sec,
            'read_count_per_sec': read_count_per_sec,
            'write_count_per_sec': write_count_per_sec
        }
    
    def get_network_info(self):
        """Return network statistics."""
        current_net_io = psutil.net_io_counters()
        current_time = time.time()
        
        # Calculate time difference
        time_diff = current_time - self.prev_net_time
        
        # Calculate rates
        bytes_sent_per_sec = (current_net_io.bytes_sent - self.prev_net_io.bytes_sent) / time_diff
        bytes_recv_per_sec = (current_net_io.bytes_recv - self.prev_net_io.bytes_recv) / time_diff
        
        # Update previous values
        self.prev_net_io = current_net_io
        self.prev_net_time = current_time
        
        return {
            'bytes_sent': current_net_io.bytes_sent,
            'bytes_recv': current_net_io.bytes_recv,
            'packets_sent': current_net_io.packets_sent,
            'packets_recv': current_net_io.packets_recv,
            'bytes_sent_per_sec': bytes_sent_per_sec,
            'bytes_recv_per_sec': bytes_recv_per_sec
        }
    
    def get_system_uptime(self):
        """Return system uptime in seconds."""
        return time.time() - psutil.boot_time()
    
    def get_gpu_metrics(self):
        """Get GPU metrics for Mac."""
        # Default values
        gpu_usage = 0
        gpu_power = 0
        
        try:
            if self.is_apple_silicon:
                # On Apple Silicon, try to use powermetrics to get GPU usage
                # Note: This requires sudo permissions in a real environment
                # For this example, we'll simulate with reasonable values
                
                # In a real implementation with sudo, you would use:
                # cmd = ["sudo", "powermetrics", "-n", "1", "-i", "1000", "--show-gpu", "--format", "json"]
                # output = subprocess.check_output(cmd).decode('utf-8')
                # metrics = json.loads(output)
                # gpu_usage = metrics.get('gpu', {}).get('gpu_utilization', 0)
                # gpu_power = metrics.get('gpu', {}).get('gpu_power', 0)
                
                # Simulated values based on CPU usage as a proxy
                cpu_usage = self.get_cpu_usage()
                # Simulate GPU usage as being typically 20-80% of CPU usage with some randomness
                import random
                gpu_usage = max(0, min(100, cpu_usage * random.uniform(0.2, 0.8) + random.uniform(-5, 15)))
                # Simulate GPU power between 1 and 10 watts, correlated with usage
                gpu_power = 1 + (gpu_usage / 100) * 9
            else:
                # For Intel Macs, we could try to use other tools or IOKit
                # For now, just use simulated values
                import random
                gpu_usage = random.uniform(10, 50)  # Intel GPUs typically less used
                gpu_power = random.uniform(1, 5)    # Lower power for Intel iGPUs
        
        except Exception as e:
            logger.error(f"Error getting GPU metrics: {str(e)}")
            # Return conservative estimates
            gpu_usage = 10
            gpu_power = 2
        
        return {
            'usage': gpu_usage,
            'power': gpu_power
        }
    
    def get_npu_metrics(self):
        """Get NPU (Neural Processing Unit) metrics for Apple Silicon."""
        # Default simulated values
        npu_usage = 0
        npu_power = 0
        
        try:
            if self.is_apple_silicon:
                # NPU metrics aren't directly exposed, so we'll simulate
                # This would be based on ML framework activity in a real implementation
                import random
                import math
                
                # Simulate occasional NPU usage spikes (ML/AI workloads tend to be bursty)
                # Most of the time NPU is idle, occasionally used heavily
                if random.random() < 0.2:  # 20% chance of NPU activity
                    npu_usage = random.uniform(50, 95)
                    # Power correlates with usage
                    npu_power = 0.5 + (npu_usage / 100) * 3.5  # 0.5 to 4 watts
                else:
                    npu_usage = random.uniform(0, 5)  # Mostly idle
                    npu_power = 0.1 + (npu_usage / 100) * 0.4  # 0.1 to 0.5 watts when idle
        
        except Exception as e:
            logger.error(f"Error getting NPU metrics: {str(e)}")
        
        return {
            'usage': npu_usage,
            'power': npu_power
        }
    
    def get_cpu_power(self):
        """Estimate CPU power usage."""
        cpu_power = 0
        
        try:
            # Get CPU load
            cpu_percent = self.get_cpu_usage()
            
            if self.is_apple_silicon:
                # Apple Silicon Macs (M1/M2/M3) have different power profiles
                # Base power around 1-2W, max around 20-30W depending on model
                # This is a very rough estimate
                cpu_power = 1.5 + (cpu_percent / 100) * 18.5  # 1.5W idle, up to 20W at full load
            else:
                # Intel Macs typically use more power
                # Base power around 3-5W, max around 45-65W for MacBook Pros
                cpu_power = 4 + (cpu_percent / 100) * 41  # 4W idle, up to 45W at full load
        
        except Exception as e:
            logger.error(f"Error estimating CPU power: {str(e)}")
            # Default conservative value
            cpu_power = 10
        
        return cpu_power
    
    def update_prometheus_metrics(self):
        """Update all Prometheus metrics with current values."""
        # CPU metrics
        cpu = self.get_cpu_usage()
        CPU_USAGE.set(cpu)
        
        # CPU power
        cpu_power = self.get_cpu_power()
        CPU_POWER.set(cpu_power)
        
        # Memory metrics
        memory = self.get_memory_usage()
        MEMORY_TOTAL.set(memory['total'])
        MEMORY_AVAILABLE.set(memory['available'])
        MEMORY_USED.set(memory['used'])
        MEMORY_PERCENT.set(memory['percent'])
        
        # Disk metrics
        disk = self.get_disk_usage()
        DISK_TOTAL.set(disk['total'])
        DISK_USED.set(disk['used'])
        DISK_FREE.set(disk['free'])
        DISK_PERCENT.set(disk['percent'])
        
        # Disk I/O metrics
        disk_io = self.get_disk_io()
        DISK_READ_BYTES.set(disk_io['read_bytes_per_sec'])
        DISK_WRITE_BYTES.set(disk_io['write_bytes_per_sec'])
        DISK_READ_IOPS.set(disk_io['read_count_per_sec'])
        DISK_WRITE_IOPS.set(disk_io['write_count_per_sec'])
        
        # Network metrics
        network = self.get_network_info()
        NETWORK_BYTES_SENT.set(network['bytes_sent'])
        NETWORK_BYTES_RECV.set(network['bytes_recv'])
        NETWORK_PACKETS_SENT.set(network['packets_sent'])
        NETWORK_PACKETS_RECV.set(network['packets_recv'])
        NETWORK_BYTES_SENT_PER_SEC.set(network['bytes_sent_per_sec'])
        NETWORK_BYTES_RECV_PER_SEC.set(network['bytes_recv_per_sec'])
        
        # GPU metrics
        gpu = self.get_gpu_metrics()
        GPU_USAGE.set(gpu['usage'])
        GPU_POWER.set(gpu['power'])
        
        # NPU metrics
        npu = self.get_npu_metrics()
        NPU_USAGE.set(npu['usage'])
        NPU_POWER.set(npu['power'])
        
        # System uptime
        uptime = self.get_system_uptime()
        SYSTEM_UPTIME.set(uptime)
        
        return {
            'cpu': cpu,
            'cpu_power': cpu_power,
            'memory': memory,
            'disk': disk,
            'disk_io': disk_io,
            'network': network,
            'gpu': gpu,
            'npu': npu,
            'uptime': uptime
        }
    
    def monitor(self, interval=5, duration=None):
        """
        Monitor system resources at specified intervals.
        
        Args:
            interval: Time between measurements in seconds
            duration: Total monitoring duration in seconds (None for indefinite)
        """
        start_time = time.time()
        counter = 0
        
        try:
            while True:
                counter += 1
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Collect and update metrics
                metrics = self.update_prometheus_metrics()
                
                # Log metrics
                logger.info(f"[{current_time}] CPU: {metrics['cpu']}% | Memory: {metrics['memory']['percent']}% | GPU: {metrics['gpu']['usage']:.1f}% | NPU: {metrics['npu']['usage']:.1f}%")
                
                # Detailed logging every 5 iterations
                if counter % 5 == 0:
                    logger.info(f"[DETAILED] CPU Power: {metrics['cpu_power']:.2f}W | GPU Power: {metrics['gpu']['power']:.2f}W | Disk: {metrics['disk']['percent']}% | Network: Sent {metrics['network']['bytes_sent_per_sec']/1024/1024:.2f}MB/s, Received {metrics['network']['bytes_recv_per_sec']/1024/1024:.2f}MB/s")
                
                # Check if monitoring duration has been reached
                if duration and (time.time() - start_time >= duration):
                    logger.info(f"Monitoring completed after {duration} seconds")
                    break
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        except Exception as e:
            logger.error(f"Error during monitoring: {str(e)}")

# Flask routes for Prometheus metrics
@app.route('/metrics')
def metrics():
    """Endpoint to expose Prometheus metrics."""
    return Response(generate_latest(REGISTRY), mimetype=CONTENT_TYPE_LATEST)

@app.route('/health')
def health():
    """Simple health check endpoint."""
    return {"status": "healthy"}

@app.route('/')
def home():
    """Home page with basic information."""
    return """
    <h1>WebAI Monitoring Exporter</h1>
    <p>Prometheus metrics available at <a href="/metrics">/metrics</a></p>
    <p>Health check available at <a href="/health">/health</a></p>
    """

if __name__ == "__main__":
    print("WebAI System Monitoring Exporter")
    print("--------------------------------")
    
    monitor = SystemMonitor()
    print(f"Monitoring system: {monitor.system_info['platform']} {monitor.system_info['platform_version']} ({monitor.system_info['architecture']})")
    print(f"Data is being logged to {log_file}")
    print(f"Metrics are available at http://localhost:8000/metrics")
    
    # Start monitoring in a separate thread
    import threading
    monitor_thread = threading.Thread(target=monitor.monitor, args=(10,), daemon=True)
    monitor_thread.start()
    
    # Start Flask server
    app.run(host='0.0.0.0', port=8000)