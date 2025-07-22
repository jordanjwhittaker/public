import os
import pandas as pd

# File Paths
input_folder = r"C:\Users\Jordan Whittaker\OneDrive - UNSW\Personal\School\UNSW\Thesis\CFD\MODELS\C120mm"
output_excel = r"C:\Users\Jordan Whittaker\Desktop\full_simulation_table.xlsx"

# Design Parameters
aoa_values = [[0, 5, 10, 12.5, 14, 15, 16, 17, 17.5, 18, 18.5, 19, 19.5, 20, 21, 22, 23.5, 25, 27.5, 30],
              [0, 5, 10, 12.5, 14, 15, 16, 17, 17.5, 18, 18.5, 19, 19.5, 20, 21, 22, 23.5, 25, 27.5, 30],
              [0, 5, 10, 12.5, 15, 18.5, 20, 21, 22, 22.5, 23, 23.5, 24, 24.5, 25, 26, 27, 28, 29, 30],
              [0, 5, 10, 12.5, 14, 15, 16, 17, 17.5, 18, 18.5, 19, 19.5, 20, 21, 22, 23.5, 25, 27.5, 30]]
velocities = [6.110736, 12.22147, 61.10736, 122.2147]

# Data table format
columns = [
    "No", "Filename", "Name", "Airfoil", "Serration", "Wavelength (^−1)", "Amplitude", "Termination",
    "Span", "Chord (mm)", "Created", "Completed", "Sim Type", "Velocity", "AOA", "Index",
    "Lift (N)", "Lift Ceof", "Drag (N)", "Drag Coef", "Moment (Nm)", "Moment Coef", "Step No.", "Converged"
]

all_rows = []
row_no = 1

# Read and parse all models
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".step"):
        name = os.path.splitext(filename)[0]
        parts = name.split("_")

        try:
            airfoil = parts[0]
            serration = parts[1]
            wavelength = float(parts[2].replace("W", ""))
            amplitude = float(parts[3].replace("A", ""))
            termination = float(parts[4].replace("T", ""))
            span = float(parts[5].replace("S", ""))
            chord = float(parts[6].replace("C", "").replace("mm", ""))

            # 80 rows per model
            index_counter = 1
            for v in range(len(velocities)):
                for aoa in aoa_values[v]:
                    sim_type = "Steady" if aoa in [0, 5, 10] else "Transient"
                    row = [
                        row_no,
                        filename,
                        name,
                        airfoil,
                        serration,
                        wavelength,
                        amplitude,
                        termination,
                        span,
                        chord,
                        0,  # Created
                        0,  # Completed
                        sim_type,
                        velocities[v],
                        aoa,
                        index_counter,
                        "", "", "", "", "", "",  # Lift, Lift Coef, Drag, Drag Coef, Moment, Moment Coef
                        "",  # Step No.
                        0    # Converged
                    ]
                    all_rows.append(row)
                    row_no += 1
                    index_counter += 1

        except (IndexError, ValueError) as e:
            print(f"Skipping {filename} due to error: {e}")

# Export
df = pd.DataFrame(all_rows, columns=columns)
df.to_excel(output_excel, index=False)
print(f"Exported {len(df)} rows to: {output_excel}")
