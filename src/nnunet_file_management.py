import os
import subprocess
from logging import getLogger
from utils import setup_logging

setup_logging()
log = getLogger('nnunet_file_management')

def rename_input_task001_blood():
    log.info('Renaming input files for blood pool segmentation task.')
    
    filename_mappings = {}
    identifier = 1

    input_folder = os.listdir('/input')
    for file in input_folder:
        if file.endswith('.nii.gz'):
            new_filename = 'BLOOD_' + f'00{identifier}'[-3:] + '_0000.nii.gz'
            filename_mappings[file] = new_filename
            
            subprocess.run(f'mv /input/{file} /input/{new_filename}')

            identifier += 1

    log.info(input_folder)
    log.info(filename_mappings)
    log.info(os.listdir('/input'))
