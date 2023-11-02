#!/bin/bash
#SBATCH --job-name=python3.10
#SBATCH --ntasks=1
#SBATCH -p short
#SBATCH --mem 64G
#SBATCH -c 32
#SBATCH -o slurm_python310.log
#SBATCH --output=job_python310_output.txt
#SBATCH --error=job_python310_error.txt

module load Python/3.10.8
python --version
python -m venv $HOME/ambiente_teste
source $HOME/ambiente_teste/bin/activate
pip install tensorflow
python $HOME/tensorflow_Test_cluster/cifar_test.py
