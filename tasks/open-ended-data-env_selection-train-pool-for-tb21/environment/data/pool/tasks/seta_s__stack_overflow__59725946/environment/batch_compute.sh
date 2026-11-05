#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=40
#SBATCH --mem=200G
#SBATCH -o /home/researcher/logs/compute_%j.out
python3 /home/researcher/scripts/compute.py
