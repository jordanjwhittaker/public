Automation Workflow

Setup data file with: CREATE_DATA_TABLE.py (creates: ex. DATA.xlsx)
Create a new temp job folder with: NEW_JOB.py
Setup the array job with: ARRAY_JOB_GENERATOR.py (creates: ex. NACA2412_SIN_W2.5_A0.0025_T0.35_S2_C120mm_41-60_submit.sh & ex. 52_jounral.wbjn)
Upload and submit array job to the HPC cluster
Scrape the report files off the cluster with: SCRAPE_RESULTS.py
Collect and process the data files with: PROCESS_RESULTS.py
