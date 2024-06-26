import re


def extract_execution_times(log_file_path):
    destination_times = {}
    total_execution_time = None

    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            dest_match = re.search(
                r'Execution time for (.*): (\d+(\.\d+)?) seconds', line)
            total_match = re.search(r'Execution time: (\d+(\.\d+)?) seconds',
                                    line)

            if dest_match:
                destination = dest_match.group(1)
                time_taken = float(dest_match.group(2))
                destination_times[destination] = time_taken
            elif total_match:
                total_execution_time = float(total_match.group(1))

    return destination_times, total_execution_time


def print_execution_times(destination_times, total_execution_time):
    print("Execution times for each destination:")
    for destination, time_taken in destination_times.items():
        print(f"\n{destination}: {time_taken:.2f} seconds")

    if total_execution_time is not None:
        print(f"\nTotal execution time: {total_execution_time:.2f} seconds")
    else:
        print("\nTotal execution time: Not available")


if __name__ == "__main__":
    log_file_path = 'info.log'  # Path to your log file
    destination_times, total_execution_time = extract_execution_times(
        log_file_path)

    print_execution_times(destination_times, total_execution_time)
