#!/bin/bash
# More safety, by turning some bugs into errors.
# Without `errexit` you don’t need ! and can replace
# PIPESTATUS with a simple $?, but I don’t do that.
set -o errexit -o pipefail -o noclobber -o nounset

echo "[INFO - entrypoint] Starting entrypoint script for TESSLA"

export RESULTS_FOLDER="/tessla/models/nnUNet_trained_models"

#for file in *_h.png
#do
#  mv "$file" "${file/_h.png/_half.png}"
#done

echo "[INFO - entrypoint] Starting TESSLA pipeline"
python3 /tessla/src/main.py