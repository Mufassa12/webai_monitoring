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
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python webai_monitoring.py`

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

## License

Private repository - All rights reserved.