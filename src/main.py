import os
import subprocess
import utils.nnunet_file_management as nnunet_file_management
import utils.iir as iir
import utils.scar_union as scar_union

from logging import getLogger
from utils import setup_logging


setup_logging()
log = getLogger('main')

def main():
    # map input files to nnUNet file convention
    nnunet_file_management.prepare_input_files()

    # run nnUNet model for Task001_Blood
    log.info('Running Task001_Blood ...')
    subprocess.run(['nnUNet_predict', '-i', '/input_Task001_Blood', '-o', '/output_Task001_Blood', '-t', 'Task001_Blood', '-m', '3d_fullres', '-f', '0'])

    # IIR normalization and preparing input data for Task003_Scar
    iir.iir_processing()

    # run nnUNet model for Task003_Scar
    log.info('Running Task003_Scar ...')
    subprocess.run(['nnUNet_predict', '-i', '/input_Task003_Scar', '-o', '/output_Task003_Scar', '-t', 'Task003_Scar', '-m', '3d_fullres', '-f', '0'])

    # run nnUNet model for Task002_Scar
    log.info('Running Task002_Scar ...')
    subprocess.run(['nnUNet_predict', '-i', '/input_Task002_Scar', '-o', '/output_Task002_Scar', '-t', 'Task002_Scar', '-m', '3d_fullres', '-f', '0'])

    # combine scar predictions from Task002_Scar and Task003_Scar
    scar_union.generate_final_scar_prediction()

    log.info('\nFINISHED! Results are saved in /output directory')
    log.info(f"/output:\n{os.listdir('/output')}\n")

if __name__ == "__main__":
    main()
