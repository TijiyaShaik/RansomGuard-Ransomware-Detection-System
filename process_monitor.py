import psutil


class ProcessMonitor:

    def get_process_details(self):

        processes = []

        for process in psutil.process_iter(
            ["pid", "name", "username"]
        ):

            try:

                details = process.info

                processes.append({
                    "pid": details["pid"],
                    "name": details["name"],
                    "username": details["username"]
                })

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied
            ):
                continue

        return processes


if __name__ == "__main__":

    monitor = ProcessMonitor()

    processes = monitor.get_process_details()

    print("\nRUNNING PROCESSES")

    for process in processes[:20]:

        print(
            "PID:", process["pid"],
            "| Name:", process["name"]
        )