class SystemMonitor:
    def __init__(self):
        import os
        import time
        import psutil
        import platform
        import logging
        from datetime import datetime
        from prometheus_client import start_http_server, Gauge

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename='webai_monitoring.log'
        )

        logger = logging.getLogger('WebAI-Monitor')

        self.system_info = {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'hostname': platform.node()
        }
        logger.info(f"System Monitor initialized on {self.system_info['hostname']}")

        # Prometheus metrics
        self.cpu_usage_gauge = Gauge('cpu_usage', 'CPU usage percentage')
        self.memory_usage_gauge = Gauge('memory_usage_percent', 'Memory usage percentage')
        self.disk_usage_gauge = Gauge('disk_usage_percent', 'Disk usage percentage')

    def get_cpu_usage(self):
        """Return the CPU usage as a percentage."""
        return psutil.cpu_percent(interval=1)

    def get_memory_usage(self):
        """Return memory usage statistics."""
        memory = psutil.virtual_memory()
        return memory.percent

    def get_disk_usage(self):
        """Return disk usage statistics."""
        disk = psutil.disk_usage('/')
        return disk.percent

    def monitor(self):
        """Monitor system resources and expose metrics."""
        while True:
            self.cpu_usage_gauge.set(self.get_cpu_usage())
            self.memory_usage_gauge.set(self.get_memory_usage())
            self.disk_usage_gauge.set(self.get_disk_usage())
            time.sleep(10)

if __name__ == "__main__":
    monitor = SystemMonitor()
    start_http_server(8000)
    monitor.monitor()