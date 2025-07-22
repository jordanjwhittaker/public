import pandas as pd
import os
import shutil
import csv

# Paths
excel_path = r"C:\Users\Jordan Whittaker\OneDrive - UNSW\Personal\School\UNSW\Thesis\CFD\RESULTS\DATA (DO NOT TOUCH).xlsx"
backup_path = r"C:\Users\Jordan Whittaker\OneDrive - UNSW\Personal\School\UNSW\Thesis\CFD\RESULTS\DATA (BACKUP).xlsx"
new_folder = r"C:\Users\Jordan Whittaker\OneDrive - UNSW\Personal\School\UNSW\Thesis\CFD\RESULTS\NEW\CSVs"
processed_folder = r"C:\Users\Jordan Whittaker\OneDrive - UNSW\Personal\School\UNSW\Thesis\CFD\RESULTS\PROCESSED\CSVs"

# Load and then backup data file
df = pd.read_excel(excel_path)
df.to_excel(backup_path, index=False)

os.makedirs(processed_folder, exist_ok=True)

# Process data files
for filename in os.listdir(new_folder):
    if filename.endswith(".csv") and "_" in filename:
        try:
            name, index_str = filename.replace(".csv", "").rsplit("_", 1)
            index = int(index_str)

            # Read CSV data
            csv_path = os.path.join(new_folder, filename)
            csv_data = pd.read_csv(csv_path, delimiter=",", skiprows=6)

            # Extract values
            clift_val = csv_data.iloc[0, 3]
            lift_val = csv_data.iloc[0, 4]
            drag_val = csv_data.iloc[0, 5]
            cdrag_val = csv_data.iloc[0, 6]
            moment_val = csv_data.iloc[0, 7]
            cmoment_val = csv_data.iloc[0, 8]

            mask = (df["Name"] == name) & (df["Index"] == index)
            df.loc[mask, ["Drag (N)", "Drag Coef", "Lift (N)", "Lift Ceof", "Moment (Nm)", "Moment Coef"]] = [
                pd.to_numeric(drag_val, errors="coerce"),
                pd.to_numeric(cdrag_val, errors="coerce"),
                pd.to_numeric(lift_val, errors="coerce"),
                pd.to_numeric(clift_val, errors="coerce"),
                pd.to_numeric(moment_val, errors="coerce"),
                pd.to_numeric(cmoment_val, errors="coerce")
            ]
            df.loc[mask, "Completed"] = 1

            # Move processed file
            shutil.move(csv_path, os.path.join(processed_folder, filename))
            print(f"✅ Processed: {filename}")

        except Exception as e:
            print(f"Failed to process {filename}: {e}")

# Ensure all data is number format
cols = ["Drag (N)", "Drag Coef", "Lift (N)", "Lift Ceof", "Moment (Nm)", "Moment Coef"]
df[cols] = df[cols].apply(pd.to_numeric, errors="coerce")

df.to_excel(excel_path, index=False)
print("All files processed and Excel updated.")
