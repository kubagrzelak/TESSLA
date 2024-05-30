# TESSLA

Two-Stage Ensemble Scar Segmentation for the Left Atrium proposed for the [LAScarQS 2022: Left Atrial and Scar Quantification & Segmentation Challenge in conjunction with STACOM and MICCAI 2022 (Sep 18th, 2022, Singapore)](https://zmiclab.github.io/projects/lascarqs22/index.html).

TESSLA Paper Preprint: DOI: [10.1007/978-3-031-31778-1_10](https://link.springer.com/chapter/10.1007/978-3-031-31778-1_10)

## Tasks

* Task001_Blood -> Segmentation of left atrium blood pool from LGE-MRI
* Task002_Scar -> Segmentation of left atrium scars from LGE-MRI
* Task003_Scar -> Segmentation of left atrium scars from IIR wall

## Docker Pipeline

Docker image implementation supports both GPU and CPU modes. We recommend running Docker image with GPU as it takes approximately 6 min per subject on our machine (NVIDIA GeForce RTX 3060 and 16GB RAM) versus 2h per subject in CPU mode (12th Gen Intel(R) Core(TM) i7-12700KF 3.61 GHz).

To run GPU version of the code have NVIDIA Container Toolkit installed to the host machine and add '--gpus all' flag to docker run command, here is an example command:

`docker run --gpus all -v <our_test_directory>:/input:ro -v :/output -it ai4af/tessla:latest`

Our docker image does not require running additional commands.

## Running TESSLA

Navigate to TESSLA root directory and run the following commands:

* Create a Docker image: `make create_image`
* Run the Docker image: `make run_image`

The predicted left atrium bloodpool and scar segmentations are saved in Docker container `/output` folder, so the folder should be copied to the host machine at the end of the process.
