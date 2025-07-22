import os
import shutil
from datetime import datetime

# File path
source_folder = r"C:\Users\Jordan Whittaker\OneDrive - UNSW\Personal\School\UNSW\Thesis\CFD\BASE SIM"
desktop = os.path.join(os.path.expanduser("~"), "Desktop")

# Create unique time-stamped temp job
timestamp = datetime.now().strftime("%S%M%H_%d%m%Y")
temp_job_folder = os.path.join(desktop, f"temp_job_{timestamp}")

# Copy all files
shutil.copytree(source_folder, temp_job_folder)

print(f"Copied '{source_folder}' to '{temp_job_folder}'")