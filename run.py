import json
import time
import schedule
from monitor import SystemMonitor
from logger import HealthLogger
from alerts import AlertManager


def load_config():
    with open("config.json", "r") as f:
        return json.load(f)


def run_health_check(monitor, logger, alert_mgr, config):
    print("Running health check...")
    metrics = monitor.get_metrics()
    logger.log_metrics(metrics)

    thresholds = config.get("thresholds", {})
    alerts = []

    if metrics["cpu_percent"] > thresholds.get("cpu_percent", 90):
        alerts.append(f"High CPU: {metrics['cpu_percent']}%")
    if metrics["memory_percent"] > thresholds.get("memory_percent", 90):
        alerts.append(f"High Memory: {metrics['memory_percent']}%")
    if metrics["disk_percent"] > thresholds.get("disk_percent", 90):
        alerts.append(f"Low Disk Space: {metrics['disk_percent']}% used")

    if metrics["swap_percent"] > thresholds.get("swap_percent", 80):
        alerts.append(
            f"High Swap Usage: {metrics['swap_percent']}% (System may be paging heavily)"
        )
    if metrics["load_percent"] > thresholds.get("load_percent", 100):
        alerts.append(f"High Load Average: {metrics['load_percent']}%")

    if alerts:
        subject = "CRITICAL: System Health Alert"

        # Format the top CPU processes
        cpu_process_str = "\n".join(
            [
                f"- {p['name']} (PID: {p['pid']}): {p['cpu_percent']}% CPU"
                for p in metrics["top_processes_cpu"]
            ]
        )

        # Format the top Memory processes
        mem_process_str = "\n".join(
            [
                f"- {p['name']} (PID: {p['pid']}): {p['memory_percent']}% RAM"
                for p in metrics["top_processes_memory"]
            ]
        )

        body = f"""System Health Alert Triggered!

Alerts:
{chr(10).join(alerts)}

System Status:
- Uptime: {metrics['uptime_hours']} hours
- Load Avg (1m, 15m): {metrics['load_1']}, {metrics['load_15']}
- CPU Usage: {metrics['cpu_percent']}%
- RAM Usage: {metrics['memory_percent']}%
- Swap Usage: {metrics['swap_percent']}%
- Disk Usage: {metrics['disk_percent']}%

Top CPU Consuming Processes:
{cpu_process_str}

Top Memory Consuming Processes:
{mem_process_str}
"""
        alert_mgr.send_email_alert(subject, body)
        alert_mgr.send_webhook_alert({"alerts": alerts, "metrics": metrics})


def main():
    config = load_config()
    monitor = SystemMonitor()
    logger = HealthLogger()
    alert_mgr = AlertManager(config)

    # Run once immediately
    run_health_check(monitor, logger, alert_mgr, config)

    # Schedule the job
    interval = config.get("thresholds", {}).get("check_interval_minutes", 1)
    schedule.every(interval).minutes.do(
        run_health_check, monitor, logger, alert_mgr, config
    )

    print(
        f"Monitoring started. Checking every {interval} minute(s). Press Ctrl+C to stop."
    )
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
