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

## License

Private repository - All rights reserved.