import tkinter as tk
import subprocess
import os
import threading

current_process = None
terminate_signal = threading.Event()  # Event to signal thread termination


def run_bash_script():
    global current_process
    
    # Path to your Bash script
    bash_script_path = "./script.sh"

    # Ensure the script is executable
    os.chmod(bash_script_path, 0o755)

    def execute_script():
        global current_process
        
        # Reset the termination signal
        terminate_signal.clear()
        
        # Start the Bash script
        current_process = subprocess.Popen(bash_script_path, shell=True)

        # Loop until the process ends or termination signal is set
        while not terminate_signal.is_set():
            if current_process.poll() is not None:
                break
            threading.Event().wait(0.1)  # Avoid busy-waiting

        # If the signal is set, ensure the process is terminated
        if terminate_signal.is_set() and current_process:
            current_process.terminate()
            current_process.wait()  # Wait for the process to fully stop

    # Start the Bash script in a new thread
    thread = threading.Thread(target=execute_script)
    thread.start()


def stop_bash_script():
    global current_process
    
    if current_process:
        # Set the termination signal to stop the thread
        terminate_signal.set()

        # Ensure the process is terminated
        current_process.terminate()
        current_process.wait()  # Ensure full termination
        current_process = None  # Clear reference

        print("Script has stopped.")


def close_application():
    # Stop the Bash script if it's running
    stop_bash_script()

    # Ensure the process reference is cleared
    global current_process
    if current_process:
        current_process = None

        os.system("clear")
    # Exit the Tkinter application
    root.quit()
    # Close the Tkinter window
    root.destroy()


# Create the Tkinter GUI
SIZE = "600x400"
root = tk.Tk()
root.geometry(SIZE)

# Button to run the Bash script
tk.Button(root, text="Activate", command=run_bash_script).pack(pady=10)

# Button to stop the Bash script
tk.Button(root, text="Deactivate", command=stop_bash_script).pack(pady=10)

# Button to exit the application
tk.Button(root, text="Exit", command=close_application).pack(pady=10)

# Run the Tkinter event loop
root.mainloop()

