import psutil
import time
import csv
import os
from datetime import datetime

def monitor_performance(interval_seconds=5, log_file="performance_log.csv", duration_minutes=None):
    """
    Monitors CPU and memory usage and logs it to a CSV file.
    """
    print(f"Starting system performance monitoring. Data will be logged to '{log_file}'.")
    print(f"Monitoring interval: {interval_seconds} seconds.")
    if duration_minutes:
        print(f"Monitoring duration: {duration_minutes} minutes.")
    else:
        print("Monitoring will run indefinitely. Press Ctrl+C to stop.")

    # Check if the log file exists to determine if a header is needed
    file_exists = os.path.exists(log_file)

    try:
        with open(log_file, 'a', newline='') as f:
            writer = csv.writer(f)

            # Write header only if the file is new
            if not file_exists:
                writer.writerow(["Timestamp", "CPU_Usage_Percent", "Memory_Usage_Percent"])
                print("CSV header written.")

            start_time = time.time()

            while True:
                try:
                    # Get current timestamp
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Get CPU usage percentage
                    cpu_percent = psutil.cpu_percent(interval=None) # Non-blocking call

                    # Get memory usage percentage
                    memory_info = psutil.virtual_memory()
                    memory_percent = memory_info.percent

                    # Log the data
                    writer.writerow([timestamp, cpu_percent, memory_percent])
                    f.flush() # Ensure data is written to disk immediately

                    print(f"Logged: {timestamp} - CPU: {cpu_percent:.2f}% | Memory: {memory_percent:.2f}%")

                    # Check if duration limit is reached
                    if duration_minutes:
                        elapsed_time = (time.time() - start_time) / 60
                        if elapsed_time >= duration_minutes:
                            print(f"Monitoring completed after {duration_minutes} minutes.")
                            break

                    # Wait for the next interval
                    time.sleep(interval_seconds)

                except Exception as e:
                    print(f"An error occurred during data collection: {e}")
                    time.sleep(interval_seconds) # Still wait before retrying

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user (Ctrl+C).")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
   
    monitor_performance(interval_seconds=2, log_file="my_system_stats.csv")

