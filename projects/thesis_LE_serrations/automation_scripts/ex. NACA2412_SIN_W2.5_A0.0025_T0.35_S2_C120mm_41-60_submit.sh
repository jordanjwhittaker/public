#!/bin/bash

#PBS -N NACA2412_SIN_W2.5_A0.0025_T0.35_S2_C120mm
#PBS -J 41-60
#PBS -l select=1:ncpus=32:mem=183gb
#PBS -l walltime=12:00:00
#PBS -j oe
#PBS -m ae
#PBS -M z5363798@unsw.edu.au

# Load ANSYS module
module load ansys/2024R2

# Change to your working directory
cd /srv/scratch/z5363798/SIMULATIONS/NACA2412_SIN_W2.5_A0.0025_T0.35_S2_C120mm/${PBS_ARRAY_INDEX}

# Run Workbench in batch mode with parametric solve and export
runwb2 -B -R ${PBS_ARRAY_INDEX}_journal.wbjn
