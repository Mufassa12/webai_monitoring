from flask import Flask, Response
from prometheus_client import generate_latest, CollectorRegistry
from webai_monitoring import SystemMonitor

app = Flask(__name__)
monitor = SystemMonitor()

@app.route('/metrics')
def metrics():
    registry = CollectorRegistry()
    
    # Collect metrics
    cpu_usage = monitor.get_cpu_usage()
    memory_usage = monitor.get_memory_usage()
    disk_usage = monitor.get_disk_usage()
    network_info = monitor.get_network_info()
    
    # Prepare metrics for Prometheus
    metrics_data = f"""
# HELP cpu_usage CPU usage percentage
# TYPE cpu_usage gauge
cpu_usage {cpu_usage}

# HELP memory_usage Memory usage percentage
# TYPE memory_usage gauge
memory_usage {memory_usage['percent']}

# HELP disk_usage Disk usage percentage
# TYPE disk_usage gauge
disk_usage {disk_usage['percent']}

# HELP bytes_sent Total bytes sent over the network
# TYPE bytes_sent counter
bytes_sent {network_info['bytes_sent']}

# HELP bytes_recv Total bytes received over the network
# TYPE bytes_recv counter
bytes_recv {network_info['bytes_recv']}
"""
    return Response(metrics_data, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)