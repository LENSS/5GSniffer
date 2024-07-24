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
    
def execute_command_and_wait(command):
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        # Print the command output
        print("Command Output:\n", result.stdout)
        # Print the error (if any)
        if result.stderr:
            print("Command Error:\n", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def terminate_command(process):
    try:
        # Terminate the process group to ensure all child processes are killed
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        print("Command terminated successfully.")
    except Exception as e:
        print(f"An error occurred while terminating the command: {e}")

video_urls = ["https://www.youtube.com/watch?v=kJQP7kiw5Fk",
"https://www.youtube.com/watch?v=RgKAFK5djSk",
"https://www.youtube.com/watch?v=JGwWNGJdvx8",
"https://www.youtube.com/watch?v=OPf0YbXqDm0",
"https://www.youtube.com/watch?v=9bZkp7q19f0" ]
iterations = 5
rnti_ragne = [29606, 29606]
scrambling_id_ragne = [9202, 9202]

for vn, url in enumerate(video_urls):
    for i in range(iterations): # iteration number
        ## Play Youtube video and collect data         
        sdr_process = execute_command("uhd_rx_cfile -r 23040000 -f 626450000  /tmp/n71.fc32")
        time.sleep(2) # give some time for setting sdr
        youtube_process = execute_command(f"google-chrome {url}")
        time.sleep(90) # data collection time
        terminate_command(sdr_process)
        terminate_command(youtube_process)
        
        ## Get DCI information
        process = execute_command_and_wait(f"python3 generate_config.py --rnti_start {rnti_ragne[0]} --rnti_end {rnti_ragne[1]} --scrambling_id_start {scrambling_id_ragne[0]} --scrambling_id_end {scrambling_id_ragne[1]}")
        process = execute_command_and_wait(f"/home/swlee/workspace/5GSniffer/5gsniffer/build/src/5g_sniffer ./config.toml > ../collected_data/output_{vn}_{i}.txt")

# %%
