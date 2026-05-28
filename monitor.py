#!/usr/bin/env python3
import psutil
import time
from datetime import datetime


class SystemMonitor:
    """Collects system health metrics."""

    def __init__(self):
        # Store boot time once when the monitor starts
        self.boot_time = psutil.boot_time()

    def get_metrics(self):
        # 1. Basic Metrics
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        # 2. Swap Memory
        swap = psutil.swap_memory()

        # 3. Load Average (with Windows fallback)
        try:
            load_1, load_5, load_15 = psutil.getloadavg()
            cpu_cores = psutil.cpu_count() or 1
            load_percent = (load_1 / cpu_cores) * 100
        except AttributeError:
            # Fallback if getloadavg() is unsupported on a specific OS version
            load_1, load_5, load_15, load_percent = 0.0, 0.0, 0.0, 0.0

        # 4. Uptime
        uptime_hours = (time.time() - self.boot_time) / 3600

        # 5. Top 3 Processes by CPU & Memory
        cpu_cores = psutil.cpu_count() or 1
        processes_pool = []

        for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            try:
                # Skip idle placeholders or processes missing data
                if p.info["cpu_percent"] is None or p.info["memory_percent"] is None:
                    continue
                if p.info["name"] in ["System Idle Process", "Idle"]:
                    continue

                processes_pool.append(p.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        # Sort and extract Top 3 for CPU 
        top_3_cpu = sorted(
            processes_pool, key=lambda x: x["cpu_percent"], reverse=True
        )[:3]
        formatted_cpu = [
            {
                "pid": p["pid"],
                "name": p["name"],
                "cpu_percent": round(p["cpu_percent"] / cpu_cores, 1),
            }
            for p in top_3_cpu
        ]

        # Sort and extract Top 3 for Memory (RAM percent is already out of 100%)
        top_3_memory = sorted(
            processes_pool, key=lambda x: x["memory_percent"], reverse=True
        )[:3]
        formatted_memory = [
            {
                "pid": p["pid"],
                "name": p["name"],
                "memory_percent": round(p["memory_percent"], 1),
            }
            for p in top_3_memory
        ]

        return {
            "cpu_percent": cpu,
            "memory_percent": memory.percent,
            "disk_percent": disk.percent,
            "swap_percent": swap.percent,
            "load_1": round(load_1, 2),
            "load_15": round(load_15, 2),
            "load_percent": round(load_percent, 2),
            "uptime_hours": round(uptime_hours, 2),
            "top_processes_cpu": formatted_cpu,
            "top_processes_memory": formatted_memory,
        }
