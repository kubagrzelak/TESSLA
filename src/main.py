import os
import subprocess
import utils.nnunet_file_management as nnunet_file_management
import utils.iir as iir
import utils.scar_union as scar_union
import datetime
import torch

from logging import getLogger
from utils import setup_logging


setup_logging()
log = getLogger('main')

def main():
    log.info(f'PYTORCH CUDA IS AVAILABLE: {torch.cuda.is_available()}')
    start_time = datetime.datetime.now()
    log.info(f'Start time: {start_time}')

    # map input files to nnUNet file convention
    nnunet_file_management.prepare_input_files()

    # run nnUNet model for Task001_Blood
    log.info('Running Task001_Blood ...')
    log.info(f"Files in /input_Task001_Blood: {os.listdir('./input_Task001_Blood')}")
    subprocess.run(['nnUNet_predict', '-i', './input_Task001_Blood', '-o', './output_Task001_Blood', '-t', 'Task001_Blood', '-m', '3d_fullres', '-f', '0'])
    log.info(f"Files in /output_Task001_Blood: {os.listdir('./output_Task001_Blood')}")

    # IIR normalization and preparing input data for Task003_Scar
    iir.iir_processing()

    # run nnUNet model for Task003_Scar
    log.info('Running Task003_Scar ...')
    log.info(f"Files in /input_Task003_Scar: {os.listdir('./input_Task003_Scar')}")
    subprocess.run(['nnUNet_predict', '-i', './input_Task003_Scar', '-o', './output_Task003_Scar', '-t', 'Task003_Scar', '-m', '3d_fullres', '-f', '0'])
    log.info(f"Files in /output_Task003_Scar: {os.listdir('./output_Task003_Scar')}")

    # run nnUNet model for Task002_Scar
    log.info('Running Task002_Scar ...')
    log.info(f"Files in /input_Task002_Scar: {os.listdir('./input_Task002_Scar')}")
    subprocess.run(['nnUNet_predict', '-i', './input_Task002_Scar', '-o', './output_Task002_Scar', '-t', 'Task002_Scar', '-m', '3d_fullres', '-f', '0'])
    log.info(f"Files in /output_Task002_Scar: {os.listdir('./output_Task002_Scar')}")

    # combine scar predictions from Task002_Scar and Task003_Scar
    scar_union.generate_final_scar_prediction()

    # save blood pool predictions from Task001_Blood
    scar_union.generate_final_blood_prediction()

    log.info('\nFINISHED! Results are saved in /output directory')
    log.info(f"/output:\n{os.listdir('../output')}\n")
    log.info(f'End time: {datetime.datetime.now()} (Start time: {start_time})')

if __name__ == "__main__":
    main()
