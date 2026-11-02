import psutil


class ProcessContainment:

    def stop_confirmed_test_process(self, pid):

        try:

            process = psutil.Process(pid)

            name = process.name()

            print("\nProcess Details")

            print("PID:", pid)
            print("Process:", name)

            confirmation = input(
                "Stop this confirmed test process? (yes/no): "
            )

            if confirmation.lower() != "yes":

                print("Containment cancelled.")

                return False

            process.terminate()

            try:
                process.wait(timeout=5)

            except psutil.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)

            print("Test process stopped successfully.")

            return True

        except psutil.NoSuchProcess:

            print("Process no longer exists.")

            return False

        except psutil.AccessDenied:

            print("Access denied. Process was not stopped.")

            return False