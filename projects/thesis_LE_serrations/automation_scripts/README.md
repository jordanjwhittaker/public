# Automation Workflow

This repository automates the end-to-end process for managing parametric ANSYS Workbench simulations on an HPC cluster using array jobs. The workflow includes data setup, job generation, submission, result scraping, and processing.

---

## 🛠️ 1. Generate the Data File

Use `CREATE_DATA_TABLE.py` to create the master data spreadsheet containing simulation parameters.

- **Output:** `DATA.xlsx` (or similar)

---

## 📂 2. Create a New Temporary Job Folder

Run `NEW_JOB.py` to generate a uniquely named job folder (e.g., with a timestamp) for simulation files.

---

## ⚙️ 3. Generate Array Job Scripts

Use `ARRAY_JOB_GENERATOR.py` to generate both the job submission script and Workbench journal files.

- **Outputs:**
  - Submit script (e.g., `NACA2412_SIN_W2.5_A0.0025_T0.35_S2_C120mm_41-60_submit.sh`)
  - Journal file (e.g., `52_journal.wbjn`)

---

## 🚀 4. Submit the Job to the HPC Cluster

Upload the generated files to your HPC cluster and submit the array job using PBS or your cluster’s job scheduler.

---

## 📥 5. Scrape Report Files from the Cluster

After simulation completion, run `SCRAPE_RESULTS.py` to download all relevant Fluent report files from the cluster.

---

## 📊 6. Process and Consolidate Results

Use `PROCESS_RESULTS.py` to process the scraped report data and consolidate it into structured formats for analysis.

---

Each script is modular and customizable to fit different parameterizations, simulation types, or data formats.
