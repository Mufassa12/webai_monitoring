# WebAI Monitoring

A monitoring tool for Web AI applications that exports system metrics to Prometheus.

## Features

- Monitors CPU, memory, disk, and network usage
- GPU and NPU metrics for Apple Silicon Macs
- Power consumption estimates
- Prometheus metrics export
- Flask web server for easy integration

## Setup

1. Clone the repository
2. Create and activate a Python virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   python webai_monitoring.py
   ```

## Metrics

Metrics are available at http://localhost:8000/metrics

### Prometheus Metrics

| Metric Name                      | Description                                 |
|----------------------------------|---------------------------------------------|
| webai_cpu_usage_percent          | CPU usage in percent                        |
| webai_cpu_power_watts            | CPU power usage in watts (estimated)        |
| webai_memory_total_bytes         | Total memory in bytes                       |
| webai_memory_available_bytes     | Available memory in bytes                   |
| webai_memory_used_bytes          | Used memory in bytes                        |
| webai_memory_usage_percent       | Memory usage in percent                     |
| webai_disk_total_bytes           | Total disk space in bytes                   |
| webai_disk_used_bytes            | Used disk space in bytes                    |
| webai_disk_free_bytes            | Free disk space in bytes                    |
| webai_disk_usage_percent         | Disk usage in percent                       |
| webai_disk_read_bytes_per_sec    | Disk read bytes per second                  |
| webai_disk_write_bytes_per_sec   | Disk write bytes per second                 |
| webai_disk_read_iops             | Disk read operations per second             |
| webai_disk_write_iops            | Disk write operations per second            |
| webai_network_bytes_sent         | Network bytes sent                          |
| webai_network_bytes_recv         | Network bytes received                      |
| webai_network_packets_sent       | Network packets sent                        |
| webai_network_packets_recv       | Network packets received                    |
| webai_net_sent_bytes_per_sec     | Network bytes sent per second               |
| webai_net_recv_bytes_per_sec     | Network bytes received per second           |
| webai_system_uptime_seconds      | System uptime in seconds                    |
| webai_gpu_usage_percent          | GPU usage in percent                        |
| webai_gpu_power_watts            | GPU power usage in watts (simulated/est.)   |
| webai_npu_usage_percent          | NPU usage in percent (simulated)            |
| webai_npu_power_watts            | NPU power usage in watts (simulated)        |

> **Note:** GPU and NPU metrics are simulated/estimated for Apple Silicon Macs. On Intel Macs, values are also simulated.

## API Endpoints

| Endpoint      | Description                                      |
|--------------|--------------------------------------------------|
| `/metrics`   | Prometheus metrics endpoint (text format)         |
| `/health`    | Health check endpoint (returns JSON status)       |
| `/`          | Home/info page with links to metrics and health   |

## Example Prometheus Scrape Config

Add this to your `prometheus.yml` scrape_configs:

```yaml
scrape_configs:
  - job_name: 'webai_monitoring'
    static_configs:
      - targets: ['localhost:8000']
```

## Example Prometheus Queries

- **CPU Usage:**
  ```promql
  webai_cpu_usage_percent
  ```
- **GPU Usage:**
  ```promql
  webai_gpu_usage_percent
  ```
- **NPU Usage:**
  ```promql
  webai_npu_usage_percent
  ```
- **System Uptime (hours):**
  ```promql
  webai_system_uptime_seconds / 3600
  ```

## Requirements

- Python 3.8+
- macOS (Apple Silicon or Intel; GPU/NPU metrics simulated on Intel)
- [psutil](https://pypi.org/project/psutil/), [Flask](https://pypi.org/project/Flask/), [prometheus_client](https://pypi.org/project/prometheus_client/)

## Issues / Contributing

Feel free to open issues or submit pull requests for improvements!

## License

Private repository - All rights reserved.