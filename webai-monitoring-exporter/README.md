# WebAI Monitoring Exporter

This project is a system monitoring tool that collects and exposes metrics related to CPU, memory, disk, and network usage. It uses Flask to serve the metrics at the `/metrics` endpoint, making it compatible with Prometheus for monitoring and alerting.

## Project Structure

```
webai-monitoring-exporter
├── src
│   ├── webai_monitoring.py   # Contains the SystemMonitor class for resource monitoring
│   ├── exporter.py           # Sets up the Flask application to serve metrics
│   └── requirements.txt      # Lists the project dependencies
├── scripts
│   ├── setup.sh              # Script to set up the virtual environment and install dependencies
│   └── run.sh                # Script to run the exporter
├── .gitignore                # Specifies files to ignore in Git
└── README.md                 # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd webai-monitoring-exporter
   ```

2. **Run the setup script:**
   This script will create a virtual environment and install the required packages.
   ```bash
   ./scripts/setup.sh
   ```

3. **Run the exporter:**
   After setting up, you can run the exporter using the following command:
   ```bash
   ./scripts/run.sh
   ```

4. **Access the metrics:**
   Once the exporter is running, you can access the metrics at:
   ```
   http://localhost:8000/metrics
   ```

## Dependencies

The project requires the following Python packages:
- Flask
- Prometheus Client
- Psutil

These dependencies are listed in `src/requirements.txt` and will be installed automatically when you run the setup script.

## Usage

The exporter will continuously monitor system resources and expose the collected metrics at the specified endpoint. You can configure Prometheus to scrape these metrics for monitoring purposes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.