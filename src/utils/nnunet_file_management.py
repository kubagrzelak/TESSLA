import os
import subprocess
import json

from logging import getLogger
from utils import setup_logging

setup_logging()
log = getLogger('nnunet_file_management')

def prepare_input_files():
    log.info('Preparing input files for Task001_Blood and Task002_Scar ...')

    #log.info(os.listdir(os.getcwd()))
    
    filename_mappings = {}
    identifier = 1

    input_folder = os.listdir('/input')
    for file in input_folder:
        if file.endswith('.nii.gz'):
            # assign a sample ID
            _id = f'00{identifier}'[-3:]
            filename_mappings[_id] = file
            
            # generate input file for Task001_Blood
            new_filename_blood = 'BLOOD_' + _id + '_0000.nii.gz'
            subprocess.run(['cp', f'/input/{file}', f'./input_Task001_Blood/{new_filename_blood}'])

            # generate input file for Task002_Scar
            new_filename_scar = 'SCAR_' + _id + '_0000.nii.gz'
            subprocess.run(['cp', f'/input/{file}', f'./input_Task002_Scar/{new_filename_scar}'])

            #log.info(f'\tFiles: {new_filename_blood} {new_filename_scar}')

            identifier += 1

    with open('/tessla/assets/filename_mappings.json', 'w') as f:
        json.dump(filename_mappings, f)

    log.info(f'Generated filenames mappings: {filename_mappings}')