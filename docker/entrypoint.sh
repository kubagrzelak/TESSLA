#!/bin/bash
# More safety, by turning some bugs into errors.
# Without `errexit` you don’t need ! and can replace
# PIPESTATUS with a simple $?, but I don’t do that.
set -o errexit -o pipefail -o noclobber -o nounset

echo "[INFO - entrypoint] Starting entrypoint script for TESSLA ..."

export RESULTS_FOLDER="/tessla/models/nnUNet_trained_models"

mkdir input_Task001_Blood
mkdir output_Task001_Blood

mkdir input_Task002_Scar
mkdir output_Task002_Scar

mkdir input_Task003_Scar
mkdir output_Task003_Scar

mkdir ../output

echo "[INFO - entrypoint] Starting TESSLA pipeline ..."
python /tessla/src/main.py