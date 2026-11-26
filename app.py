import psutil
import time
import os
from collections import Counter


def get_process_information():
    processes = []
    status_count = Counter()

    total_processes = len(psutil.pids())

    for process in psutil.process_iter(
        ["pid", "name", "status"]
    ):
        try:
            process.cpu_percent(interval=None)
            processes.append(process)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Allow CPU usage measurement to collect data
    time.sleep(0.2)

    process_details = []

    for process in processes:
        try:
            info = process.info

            cpu_usage = process.cpu_percent(interval=None)

            status = info["status"] or "Unknown"
            status_count[status] += 1

            process_details.append({
                "pid": info["pid"],
                "name": info["name"] or "Unknown",
                "status": status,
                "cpu": cpu_usage
            })

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            continue

    return total_processes, status_count, process_details


def display_processes():
    total, statuses, processes = get_process_information()

    os.system("cls" if os.name == "nt" else "clear")

    print("=" * 75)
    print("                    PYTHON PROCESS COUNTER")
    print("=" * 75)

    print("\nSYSTEM PROCESS SUMMARY")
    print("-" * 75)

    print(f"Total Processes : {total}")

    print("\nPROCESS STATUS")
    print("-" * 75)

    for status, count in sorted(statuses.items()):
        print(f"{status:<20}: {count}")

    print("\nTOP 10 PROCESSES BY CPU USAGE")
    print("-" * 75)

    print(f"{'PID':<12}{'PROCESS NAME':<35}{'CPU USAGE':<15}")
    print("-" * 75)

    top_processes = sorted(
        processes,
        key=lambda process: process["cpu"],
        reverse=True
    )[:10]

    for process in top_processes:
        print(
            f"{process['pid']:<12}"
            f"{process['name'][:32]:<35}"
            f"{process['cpu']:.2f}%"
        )

    print("\nTOTAL ACCESSIBLE PROCESS DETAILS")
    print("-" * 75)

    print(f"{'PID':<12}{'PROCESS NAME':<35}{'STATUS':<20}")
    print("-" * 75)

    for process in processes:
        print(
            f"{process['pid']:<12}"
            f"{process['name'][:32]:<35}"
            f"{process['status']:<20}"
        )

    print("\n" + "=" * 75)
    print("Refreshing every 2 seconds...")
    print("Press CTRL+C to stop.")


def monitor_processes():
    try:
        while True:
            display_processes()
            time.sleep(2)

    except KeyboardInterrupt:
        print("\n\nProcess monitoring stopped.")


if __name__ == "__main__":
    monitor_processes()