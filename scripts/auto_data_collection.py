#%%
import subprocess
import time
import os
import signal
def execute_command_with_sudo(command, password=None):
    try:
        if password:
            # Create the command to echo the password and pipe it to sudo
            full_command = f"echo {password} | sudo -S {command}"
        else:
            full_command = command

        # Start the command asynchronously
        process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Command started successfully.")
        return process

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
def execute_command(command):
    try:
        # Start the command asynchronously
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)
        print("Command started successfully.")
        return process

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def terminate_command(process):
    try:
        # Terminate the process group to ensure all child processes are killed
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        print("Command terminated successfully.")
    except Exception as e:
        print(f"An error occurred while terminating the command: {e}")

if __name__ == "__main__":
    rnti_ragne = [2278, 2278]
    scrambling_id_ragne = [9202, 9202]
    for i in range(1):
        process = execute_command("uhd_rx_cfile -r 23040000 -f 626450000  /tmp/n71.fc32")
        time.sleep(5)
        terminate_command(process)
        process = execute_command(f"python3 generate_config.py --rnti_start {rnti_ragne[0]} --rnti_end {rnti_ragne[1]} --scrambling_id_start {scrambling_id_ragne[0]} --scrambling_id_end {scrambling_id_ragne[1]}")
        time.sleep(1)
        process = execute_command(f"/home/swlee/workspace/5GSniffer/5gsniffer/build/src/5g_sniffer ./config.toml > ../collected_data/output_{i}.txt")
        time.sleep(10)
        process = execute_command("rm /tmp/n71.fc32")