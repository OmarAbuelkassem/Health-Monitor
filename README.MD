# Infrastructure Health Monitor

**An Automated System Monitoring Agent**

![Status](https://img.shields.io/badge/status-active-brightgreen) ![Python](https://img.shields.io/badge/python-3.7%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green)

A lightweight, self-contained Python agent that monitors CPU, memory, swap, and disk metrics. When thresholds are breached, it automatically triggers email or webhook alerts containing the exact processes causing the bottleneck.

## ✨ Features

- **Core Metrics:** Tracks CPU, load average, RAM, Swap, Disk, and Uptime.
- **Process Diagnostics:** Instantly identifies the Top 3 CPU and RAM consuming processes.
- **Smart Alerting:** SMTP Email and Webhook integrations with customizable thresholds.
- **Lightweight Logging:** Single-line JSON audit trails for easy parsing without the overhead.

## 🚀 Quick Start

**1. Clone & Setup Environment**

```bash
git clone [https://github.com/yourusername/health-monitor.git](https://github.com/yourusername/health-monitor.git)
cd health-monitor
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**2. Configure Thresholds**

Copy the example config and adjust your limits in config.json:
Note: webhooks are not yet implemented.

```json
{
  "thresholds": {
    "cpu_percent": 85,
    "memory_percent": 85,
    "disk_percent": 90,
    "swap_percent": 80,
    "check_interval_minutes": 1
  },
  "alerts": {
    "email_enabled": true,
    "email_to": "alerts@example.com",
    "webhook_enabled": false
  }
}
```

**3. Setup Credentials**

Create a .env file in the root directory for your email alerts (Use an App Password for Gmail):

```
ALERT_EMAIL=your@gmail.com
ALERT_PASSWORD=your_16_char_app_password
```

**4. Run the Monitor**

```python
python run.py
```

## 📂 Project Structure

```
health-monitor/
├── monitor.py           # Core psutil metrics collection
├── alerts.py            # SMTP & Webhook notification logic
├── logger.py            # JSON append-only logging
├── run.py               # Main loop and threshold evaluation
├── config.json          # System thresholds & alert routing
├── requirements.txt     # Dependencies (psutil, requests, etc.)
└── .env                 # Secret credentials (git-ignored)
```

## 🔍 Log & Alert Output

When a threshold is triggered, you receive an immediate alert formatted for quick triage:

```
System Health Alert Triggered!

Alerts:
High CPU: 13.6%
High Memory: 87.7%
Low Disk Space: 64.7% used

System Status:
- Uptime: 26.24 hours
- Load Avg (1m, 15m): 0.0, 0.0
- CPU Usage: 13.6%
- RAM Usage: 87.7%
- Swap Usage: 14.0%
- Disk Usage: 64.7%

Top CPU Consuming Processes:
- msedge.exe (PID: 6752): 6.5% CPU
- msedge.exe (PID: 18360): 2.4% CPU
- msedge.exe (PID: 18556): 1.4% CPU

Top Memory Consuming Processes:
- MemCompression (PID: 3828): 6.1% RAM
- msedge.exe (PID: 6752): 5.4% RAM
- Code.exe (PID: 16820): 5.2% RAM
```

(All checks are also permanently recorded in logs/health.log as queryable JSON).

## 📄 License

MIT License. Feel free to use, modify, and distribute.
