import os
from getpass import getpass
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient

# Configure cluster
remote_user = "z5363798"
remote_host = "katana.unsw.edu.au"
remote_base_path = "/srv/scratch/z5363798/SIMULATIONS"
local_download_path = r"C:\Users\Jordan Whittaker\OneDrive - UNSW\Personal\School\UNSW\Thesis\CFD\RESULTS\NEW"

# Report files
target_filenames = [
    "lift-rfile.out",
    "clift-rfile.out",
    "drag-rfile.out",
    "cdrag-rfile.out",
    "moment-rfile.out",
    "cmoment-rfile.out",
]

# Passwords
password = getpass(f"Enter SSH password for {remote_user}@{remote_host}: ")

# Connect to SSH
ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())
ssh.connect(remote_host, username=remote_user, password=password)
scp = SCPClient(ssh.get_transport())

# Scrape for report files
all_paths = []
for filename in target_filenames:
    cmd = f"find {remote_base_path} -type f -name '{filename}'"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    found = stdout.read().decode().splitlines()
    all_paths.extend(found)

print(f"\nFound {len(all_paths)} files.\n")

# Set naming convention and download
for remote_path in all_paths:
    rel_path = remote_path.replace(remote_base_path + "/", "")
    path_parts = rel_path.split("/")  # Expecting: ['[name]', '[index]', ...]

    try:
        name = path_parts[0]
        index = path_parts[1]
    except IndexError:
        print(f"Skipping (unexpected path structure): {remote_path}")
        continue

    original_file = os.path.basename(remote_path)
    new_filename = f"{name}_{index}_{original_file}"
    local_path = os.path.join(local_download_path, new_filename)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    print(f"Downloading {remote_path} → {new_filename}")
    scp.get(remote_path, local_path)

# Download auto-exported CSVs
remote_results_dir = "/srv/scratch/z5363798/RESULTS"
local_results_dir = r"C:\Users\Jordan Whittaker\OneDrive - UNSW\Personal\School\UNSW\Thesis\CFD\RESULTS\CSVs"

stdin, stdout, stderr = ssh.exec_command(f"find {remote_results_dir} -maxdepth 1 -type f -name '*.csv'")
csv_paths = stdout.read().decode().splitlines()

print(f"\nFound {len(csv_paths)} CSV files in RESULTS folder.\n")

for remote_csv in csv_paths:
    filename = os.path.basename(remote_csv)
    local_path = os.path.join(local_results_dir, filename)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    print(f"Downloading {remote_csv} → {filename}")
    scp.get(remote_csv, local_path)

scp.close()
ssh.close()

print("\nAll downloads complete.")
