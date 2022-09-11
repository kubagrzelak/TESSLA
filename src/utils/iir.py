import os
import numpy as np
import nibabel as nib
import datetime

from scipy import ndimage
from skimage import segmentation
from logging import getLogger
from utils import setup_logging

setup_logging()
log = getLogger('iir')

DILATION_ITER = 3

def calculate_mean_blood_pool_intensity(mri, blood_pool_mask):
    blood_pool_mask[blood_pool_mask > 0] = 1
    segmented_blood_pool = mri[blood_pool_mask == 1]
    
    return np.mean(segmented_blood_pool)

def estimate_la_wall(blood_pool_data):    
    # segment blood pool boundary 
    blood_pool_boundary = segmentation.find_boundaries(blood_pool_data, mode='thin')
    
    # Dilate the LA wall
    blood_pool_boundary_dil = ndimage.binary_dilation(blood_pool_boundary, iterations = DILATION_ITER)
    blood_pool_boundary_dil = blood_pool_boundary_dil * 1
    blood_pool_boundary_ero = ndimage.binary_erosion(blood_pool_data, iterations = DILATION_ITER)
    blood_pool_boundary_ero = blood_pool_boundary_ero * 1
    blood_pool_boundary = blood_pool_boundary_dil - blood_pool_boundary_ero
    blood_pool_boundary[blood_pool_boundary < 0] = 0
    blood_pool_boundary = blood_pool_boundary - blood_pool_data
    blood_pool_boundary[blood_pool_boundary < 0] = 0
    
    return blood_pool_boundary

def get_iir_wall(blood_pool, mri_image):
    log.info('\tExtracting IIR wall ...')
    # estimate LA wall from a blood pool prediction
    la_wall = estimate_la_wall(blood_pool)

    # Calculate blood mean intensity
    mean_bp_intensity = calculate_mean_blood_pool_intensity(mri_image, blood_pool)

    return (la_wall * mri_image) / mean_bp_intensity

def iir_processing():
    log.info('Start IIR processing ...')

    start_time = datetime.datetime.now()
    log.info(f'\tStart time: {start_time}')

    # get LGE-MRIs
    mri_files_original = os.listdir('./input_Task001_Blood')
    mri_files = []
    for file in mri_files_original:
        if file.endswith('.nii.gz'):
            mri_files.append(file)
    mri_files.sort()

    # get blood pool segmentation
    bloodpool_files_original = os.listdir('./output_Task001_Blood')
    bloodpool_files = []
    for file in bloodpool_files_original:
        if file.endswith('.nii.gz'):
            bloodpool_files.append(file)
    bloodpool_files.sort()

    for i in range(len(mri_files)):
        _id = mri_files[i][6:9]

        log.info(f'Sample: {i+1} / {len(mri_files)}     (_id: {_id})')

        # load mri file
        log.info(f'\tLoading:\t{mri_files[i]}\t{bloodpool_files[i]} ...')
        mri_nib = nib.load('./input_Task001_Blood/' + mri_files[i])
        mri = np.array(mri_nib.dataobj)
        mri = mri.astype(np.uint8)

        # load blood pool segmentation
        atrium_nib = nib.load('./output_Task001_Blood/' + bloodpool_files[i])
        atrium = np.array(atrium_nib.get_fdata())
        atrium = atrium / np.max(atrium)

        # extract IIR wall
        iir_wall = get_iir_wall(atrium, mri)

        # save files as input to Task003_Scar
        log.info('\tSaving as input to Task003_Scar ...')
        iir_wall_filename = 'SCAR_' + _id + '_0000.nii.gz'
        iir_wall = nib.Nifti1Image(iir_wall, atrium_nib.affine)
        log.info(f'\t\tIIR wall > {iir_wall_filename}')
        nib.save(iir_wall, f'./input_Task003_Scar/{iir_wall_filename}')

        mri_filename = 'SCAR_' + _id + '_0001.nii.gz'
        mri = nib.Nifti1Image(mri, mri_nib.affine)
        log.info(f'\t\tMRI > {mri_filename}')
        nib.save(mri, f'./input_Task003_Scar/{mri_filename}')

    log.info(f'End time: {datetime.datetime.now()} (Start time: {start_time})')