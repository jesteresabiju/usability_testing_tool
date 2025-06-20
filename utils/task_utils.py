import csv
import os
from datetime import datetime

def load_tasks(filepath="data/tasks.txt"):
    with open(filepath, "r") as file:
        return [line.strip() for line in file.readlines() if line.strip()]

def save_result(results, filepath="data/results_web.csv"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["task", "time_taken", "success", "start_time", "end_time"])

        for r in results:
            writer.writerow([
                r["task"],
                "%.9f" % r["time_taken"],
                str(r["success"]).upper(),
                datetime.fromtimestamp(r["start_time"]).strftime("%Y-%m-%d %H:%M:%S"),
                datetime.fromtimestamp(r["end_time"]).strftime("%Y-%m-%d %H:%M:%S"),
            ])

def calculate_summary(results):
    total = len(results)
    success = sum(1 for r in results if r["success"])
    fail = total - success
    avg_time = sum(r["time_taken"] for r in results) / total if total > 0 else 0

    return {
        "total": total,
        "success": success,
        "fail": fail,
        "avg_time": avg_time
    }
