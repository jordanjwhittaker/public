import os
import pandas as pd
import shutil

def generate_scripts(name, min_index, max_index, memory_gb, ncpus, walltime_hours, base_dir="./"):
    # PBS values
    job_range = f"{min_index}-{max_index}"
    memory = f"{memory_gb}gb"
    walltime = f"{walltime_hours:02d}:00:00"

    # Output path
    project_dir = os.path.join(base_dir, name)
    os.makedirs(project_dir, exist_ok=True)

    # Create subfolders
    for i in range(min_index, max_index + 1):
        sub_dir = os.path.join(project_dir, f"{i}")
        os.makedirs(sub_dir, exist_ok=True)

    # Submit Script
    if max_index - min_index == 0:      # For single index scripts
            submit_script = f"""#!/bin/bash

#PBS -N {name}
#PBS -l select=1:ncpus={ncpus}:mem={memory}
#PBS -l walltime={walltime}
#PBS -j oe
#PBS -m ae
#PBS -M z5363798@unsw.edu.au

# Load ANSYS module
module load ansys/2024R2

# Change to your working directory
cd /srv/scratch/z5363798/SIMULATIONS/{name}/{min_index}

# Run Workbench in batch mode with parametric solve and export
runwb2 -B -R {min_index}_journal.wbjn
"""
    else:                   # Array job for multi index scripts
        submit_script = f"""#!/bin/bash

#PBS -N {name}
#PBS -J {job_range}
#PBS -l select=1:ncpus={ncpus}:mem={memory}
#PBS -l walltime={walltime}
#PBS -j oe
#PBS -m ae
#PBS -M z5363798@unsw.edu.au

# Load ANSYS module
module load ansys/2024R2

# Change to your working directory
cd /srv/scratch/z5363798/SIMULATIONS/{name}/${{PBS_ARRAY_INDEX}}

# Run Workbench in batch mode with parametric solve and export
runwb2 -B -R ${{PBS_ARRAY_INDEX}}_journal.wbjn
"""

    steady_index = []
    transient_index = []

    for i in range(min_index, max_index + 1):
        if i % 20 in [1, 2, 3]:
            steady_index.append(i)
        else:
            transient_index.append(i)

    # Journal script for every parameter set
    for i in range(min_index, max_index + 1):
        journal_script = f"""Open(FilePath="/srv/scratch/z5363798/SIMULATIONS/{name}/{str(i)}/{str(i)}.wbpj")

designPointList = []

paras = Parameters.GetAllParameters()
dpManager = Parameters.GetAllDesignPoints()
numDPs = dpManager.Count

for p in range(numDPs):
    designPointList.append(Parameters.GetDesignPoint(Name=str(p)))

backgroundSession1 = UpdateAllDesignPoints(DesignPoints=designPointList)

Parameters.ExportAllDesignPointsData(FilePath="/srv/scratch/z5363798/RESULTS/{name}_{str(i)}.csv")

Save(Overwrite=True)
"""
        
        with open(os.path.join(project_dir, f"{str(i)}/{str(i)}_journal.wbjn"), "w") as f:
            f.write(journal_script)
            
    # ANSYS Workbench system replicator for steady-state simulations
    steady_replicator_script = f"""# encoding: utf-8
# 2024 R2
SetScriptVersion(Version="24.2.133")

# Define parameter values to sweep
indexes = {steady_index}
name = "{name}"

velocity = [None] + ([6.110736] * 20 + [12.22147] * 20 + [61.10736] * 20 + [122.2147] * 20)
AOAs = [0, 5, 10, 12.5, 14, 15, 16, 17, 17.5, 18, 18.5, 19, 19.5, 20, 21, 22, 23.5, 25, 27.5, 30]
AOA = [None] + AOAs * 4

for i in indexes:
    # Activate the design point
    dp = Parameters.GetDesignPoint(Name="0")
        
    # Get parameters by name
    parameter11 = Parameters.GetParameter(Name="P11")  # e.g., angle
    parameter1 = Parameters.GetParameter(Name="P1")  # e.g., velocity
        
    # Set parameter values
    dp.SetParameterExpression(Parameter=parameter11, Expression=str(AOA[i]) + " [degree]")
    dp.SetParameterExpression(Parameter=parameter1, Expression=str(velocity[i]) + " [m s^-1]")

    # Mark as retained
    dp.Retained = True

    # Generate export filename
    export_filename = str(i) + ".wbpj"
    export_path = r"{project_dir}" + "\\\\" + str(i) + "\\\\" + export_filename

    # Get system to export (update "FFF" to your actual system name)
    system1 = GetSystem(Name="FFF")

    # Export the system with this design point
    ExportSystems(
        Systems=[system1],
        FilePath=export_path,
        IncludeUserFiles=False,
        IncludeResultFiles=False,
        IncludeExternalFiles=False
    )
"""
    # ANSYS Workbench system replicator for transient simulations
    transient_replicator_script = f"""# encoding: utf-8
# 2024 R2
SetScriptVersion(Version="24.2.133")

# Define parameter values to sweep
indexes = {transient_index}
name = "{name}"

velocity = [None] + ([6.110736] * 20 + [12.22147] * 20 + [61.10736] * 20 + [122.2147] * 20)
AOAs = [0, 5, 10, 12.5, 14, 15, 16, 17, 17.5, 18, 18.5, 19, 19.5, 20, 21, 22, 23.5, 25, 27.5, 30]
AOA = [None] + AOAs * 4

for i in indexes:
    # Activate the design point
    dp = Parameters.GetDesignPoint(Name="0")
        
    # Get parameters by name
    parameter11 = Parameters.GetParameter(Name="P11")  # e.g., angle
    parameter1 = Parameters.GetParameter(Name="P1")  # e.g., velocity
        
    # Set parameter values
    dp.SetParameterExpression(Parameter=parameter11, Expression=str(AOA[i]) + " [degree]")
    dp.SetParameterExpression(Parameter=parameter1, Expression=str(velocity[i]) + " [m s^-1]")

    # Mark as retained
    dp.Retained = True

    # Generate export filename
    export_filename = str(i) + ".wbpj"
    export_path = r"{project_dir}" + "\\\\" + str(i) + "\\\\" + export_filename

    # Get system to export (update "FFF" to your actual system name)
    system1 = GetSystem(Name="FFF")

    # Export the system with this design point
    ExportSystems(
        Systems=[system1],
        FilePath=export_path,
        IncludeUserFiles=False,
        IncludeResultFiles=False,
        IncludeExternalFiles=False
    )
"""
    
    # Script to remind of CPU count
    core_script = f"""
{name}
ncpus = {ncpus}
"""

    # Write scripts
    with open(os.path.join(project_dir, f"{name}_{job_range}_submit.sh"), "w") as f:
        f.write(submit_script)
    with open(os.path.join(os.getcwd(), f"{name}_{job_range}_steady_replicator.wbjn"), "w") as f:
        f.write(steady_replicator_script)
    with open(os.path.join(os.getcwd(), f"{name}_{job_range}_transient_replicator.wbjn"), "w") as f:
        f.write(transient_replicator_script)
    with open(os.path.join(os.getcwd(), f"CORES_{ncpus}.txt"), "w") as f:
        f.write(core_script)

    # Copy model to temp folder
    source_dir = r"C:\Users\Jordan Whittaker\OneDrive - UNSW\Personal\School\UNSW\Thesis\CFD\MODELS\C120mm"
    target_dir = os.getcwd() 

    source_file = os.path.join(source_dir, f"{name}.step")
    target_file = os.path.join(target_dir, f"{name}.step")

    os.makedirs(target_dir, exist_ok=True)
    shutil.copy2(source_file, target_file)

    # Set all created jobs in data file to created
    df = pd.read_excel(r"C:\Users\Jordan Whittaker\OneDrive - UNSW\Personal\School\UNSW\Thesis\CFD\RESULTS\DATA (DO NOT TOUCH).xlsx")

    df.to_excel(r"C:\Users\Jordan Whittaker\OneDrive - UNSW\Personal\School\UNSW\Thesis\CFD\RESULTS\DATA (BACKUP).xlsx", index=False)

    mask = (df["Name"] == name) & (df["Index"] >= min_index) & (df["Index"] <= max_index)
    df.loc[mask, "Created"] = 1

    df.to_excel(r"C:\Users\Jordan Whittaker\OneDrive - UNSW\Personal\School\UNSW\Thesis\CFD\RESULTS\DATA (DO NOT TOUCH).xlsx", index=False)


    print(f"Created project folder at: {project_dir}")
    print(f"Created {max_index - min_index + 1} subdirectories.")
    print(f"submit.sh and journal.wbjn written to project folder.")


# Job inputs
if __name__ == "__main__":
    generate_scripts(
        name="NACA2412_NO_W0_A0_T0_S2_C120mm",
        min_index=1,
        max_index=80,
        memory_gb=150,
        ncpus=28,
        walltime_hours=12,
        base_dir = r"C:\Users\Jordan Whittaker\OneDrive - UNSW\Personal\School\UNSW\Thesis\CFD\SIMULATIONS\WAITING"
    )
