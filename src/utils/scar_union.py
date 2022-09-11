import json
import os
import numpy as np
import nibabel as nib

from logging import getLogger
from utils import setup_logging

setup_logging()
log = getLogger('scar_union')

def save_final_prediction_scar(final_prediction_nib, _id):
    log.info('\tSaving final scar prediction ...')

    # load filenames mappings
    f = open('/tessla/assets/filename_mappings.json')
    filename_mappings = json.load(f)

    # save the final prediction
    final_prediction_filename = 'prediction_scar_' + filename_mappings[_id]
    
    nib.save(final_prediction_nib, '../output/' + final_prediction_filename)

    log.info(f'\t\tSaved as {final_prediction_filename}')

def generate_final_scar_prediction():
    log.info('Start combining two scar predictions into the final predictions ...')

    # get files from Task002_Scar
    task002_scar_files_original = os.listdir('./output_Task002_Scar')
    task002_scar_files = []
    for file in task002_scar_files_original:
        if file.endswith('.nii.gz'):
            task002_scar_files.append(file)
    task002_scar_files.sort()

    # get files from Task003_Scar
    task003_scar_files_original = os.listdir('./output_Task003_Scar')
    task003_scar_files = []
    for file in task003_scar_files_original:
        if file.endswith('.nii.gz'):
            task003_scar_files.append(file)
    task003_scar_files.sort()

    for i in range(len(task002_scar_files)):
        _id = task002_scar_files[i][5:8]

        log.info(f'Sample: {i+1} / {len(task002_scar_files)}     (_id: {_id})')

        # load scar prediction from Task002_Scar
        log.info(f'\tLoading:\t{task002_scar_files[i]}\t{task003_scar_files[i]} ...')
        scar2_nib = nib.load('./output_Task002_Scar/' + task002_scar_files[i])
        scar2 = np.asarray(scar2_nib.dataobj)

        # load scar prediction from Task003_Scar
        scar3_nib = nib.load('./output_Task003_Scar/' + task003_scar_files[i])
        scar3 = np.asarray(scar3_nib.dataobj)
        
        # combine both scars to generate the final scar segmentation prediction
        final_prediction = scar2 + scar3
        final_prediction[final_prediction > 0] = 1

        final_prediction_nib = nib.Nifti1Image(final_prediction, scar2_nib.affine)

        save_final_prediction_scar(final_prediction_nib, _id)

def save_final_prediction_blood(final_prediction_nib, _id):
    log.info('\tSaving final blood pool predictions ...')

    # load filenames mappings
    f = open('/tessla/assets/filename_mappings.json')
    filename_mappings = json.load(f)

    # save the final prediction
    final_prediction_filename = 'prediction_blood_' + filename_mappings[_id]
    
    nib.save(final_prediction_nib, '../output/' + final_prediction_filename)

    log.info(f'\t\tSaved as {final_prediction_filename}')

def generate_final_blood_prediction():
    log.info('Loading blood pool predictions ...')

    # get files from Task001_Blood
    task001_blood_files_original = os.listdir('./output_Task001_Blood')
    task001_blood_files = []
    for file in task001_blood_files_original:
        if file.endswith('.nii.gz'):
            task001_blood_files.append(file)
    task001_blood_files.sort()

    for i in range(len(task001_blood_files)):
        _id = task001_blood_files[i][6:9]

        log.info(f'Sample: {i+1} / {len(task001_blood_files)}     (_id: {_id})')

        # load blood prediction from Task001_Blood
        log.info(f'\tLoading:\t{task001_blood_files[i]} ...')
        blood_nib = nib.load('./output_Task001_Blood/' + task001_blood_files[i])
        
        save_final_prediction_blood(blood_nib, _id)
