import tkinter as tk
import threading
import subprocess
import os

current_process = None
terminate_signal = threading.Event()  # Event to signal thread termination


# Function to run a Bash script in a separate thread
def run_bash_script():
    global current_process
    bash_script_path = "./snort_script.sh" #path for the bash script

    # Ensures the script is executable
    os.chmod(bash_script_path, 0o755)

    def execute_script():
        global current_process
        terminate_signal.clear()  # Reset the termination signal
        # Starts the Bash script
        current_process = subprocess.Popen(bash_script_path, shell=True)

        # Loop until the process ends or termination signal is set
        while not terminate_signal.is_set():
            if current_process.poll() is not None:
                break
            threading.Event().wait(0.5)  # Adjust the polling rate as needed

        if terminate_signal.is_set() and current_process:
            current_process.terminate()
            current_process.wait()  # Ensure full termination

    # Start the Bash script in a new thread
    thread = threading.Thread(target=execute_script)
    thread.start()


# Function to stop the running Bash script
def stop_bash_script():
    global current_process
    terminate_signal.set()  # Signal to stop the thread

    if current_process:
        current_process.terminate()  # Terminate the process
        current_process.wait()  # Ensure full termination
        current_process = None  # Clear the reference


# Function to read the latest line from a text file
def get_last_line(text_file_path): 

    try: 

        with open(text_file_path, 'r') as file: 

            lines = file.readlines() 

            if not lines: 

                return "The file is empty." 

  

            last_line = lines[-1] 

  

            # Extract characters between index 40 and 70 

            detected_attack = last_line[41:70] 

  

            # Remove square brackets from the extracted substring 

            detected_attack = detected_attack.replace("[", "").replace("]", "").replace("*","") 

  

            return detected_attack  # Return the cleaned substring 

  
    #errors if output is not detected or has a problem
    except FileNotFoundError: 

        return "Error: File not found." 

    except IOError: 

        return "Error: Could not read the file." 

    except IndexError: 

        return "Error: The last line is too short." 

    except Exception as e: 

        return f"Error: {e}" 



# Function to update the label with the latest line from the text file
def update_label(output_label, text_file_path):
    latest_line = get_last_line(text_file_path)
    output_label.config(text=latest_line)
    # Schedule the next update after 1 second
    output_label.after(1000, update_label, output_label, text_file_path)


# Fuction to close the application
def close_application():
    stop_bash_script()  # Stop running the bash script
    root.quit()  # Exits the application
    root.destroy()  # 


# Create the GUI
root = tk.Tk()
root.geometry("600x400")
root.title("Intrusion Detection Tool for DDoS/DoS Attacks")

text_file_path = "snort_output.txt"  #path to outpot file

# Label that displays the most recent line from the text file
output_label = tk.Label(root, text="Reading latest line...")
output_label.pack(pady=10)

# Initialize the label update
update_label(output_label, text_file_path)

# Button to run the Activate script
tk.Button(root, text="Activate", command=run_bash_script).pack(pady=10)

# Button to stop the Deactivate script
#tk.Button(root, text="Deactivate", command=stop_bash_script).pack(pady=10)

# Button to exit the application
tk.Button(root, text="Exit", command=close_application).pack(pady=10)

# Runs the Tkinter event loop
root.mainloop()
