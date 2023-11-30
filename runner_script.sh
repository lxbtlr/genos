#!/bin/bash -l

#$ -P ct-scicomp        # Specify the SCC project name you want to use
#$ -l h_rt=12:00:00      # Specify the hard time limit for the job, (120 is max, HH:MM:SS)
# Specify when an email is sent (default is none).
#$ -m beas              # currently set to send email when job: starts, ends, aborts and is suspended
#$ -N ProHC-ImgRecon    # Give job a name
#$ -j y                 # Merge the error and output streams into a single file

# Request partial node resources:
#$ -pe omp 8            # Request 8 cores
#$ -l mem_per_core=8G   # Request 8GB of RAM



export PYTHONPATH=/project/ct-scicomp/pythonlibs/lib/python3.9/site-packages/:$PYTHONPATH
export PATH=/project/ct-scicomp/pythonlibs/bin:$PATH
# Unclear what this line does / why we would need this added to path
# export PATH=/project/ct-scicomp/find_orb_lib/find_orb:/$PATH

module load python3/3.9.9
python3 model.py --max_polygons 30 --max_evaluations 50000 --stagnation_limit 50 --base_image  --output_image
# add correct args for script


# qsub runner_script.sh
# qstat -u USERID
# qdel PID
