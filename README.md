# python_scheduler

# Purpose: (copied from https://github.com/ncsa/Scheduler)
The purpose of Scheduler is to help user to submit large number of independent jobs into the queue on HPC sites in the form of a single job.

On HPC sites, the job submission is managed by resource managers like Torque or PBS, which are batch queuing systems. The job submission is tailored toward submitting parallel MPI jobs that may use from a few to thousands of compute nodes per application. The job is submitted to the queue with help of a qsub command. Each submitted job obtains a jobid.

In the situation when user needs to handle thousands of single-node jobs vs a single job that can use a thousand of nodes, the use of batch queuing system becomes cumbersome. For instance, in order to submit 1000 single node-jobs, a user has to prepare a separate batch script for each individual job and type qsub command 1000 times. This would queue 1000 independed jobs into the queue. However, on many HPC sites there are limits on how many jobs user may submit into the queue. The cap on the number of jobs that can accumulate priority in the queue is typically around 50.

Scheduler allows user to aggregate the independent single-core jobs under a single batch job. That means user can submit a single job bundling up any number of small jobs into a single job with help of a very simple configuration file.



                    
# Jobs File
Example File 
```
cd /home/username/project1/; ./tool.pl -param1 True -data /home/username/datasets/data1 
cd /home/username/project1/; ./tool.pl -param1 True -data /home/username/datasets/data2 
cd /home/username/project1/; ./tool.pl -param1 False -data /home/username/datasets/data3 
cd /home/username/project1/; ./tool.pl -param1 True -data /home/username/datasets/dataN  
```

# Parameters

```
--cpu The number of cpus that each job takes
--mem The number of memory that each job takes (estimated)
--log The log file directory
--hostfile List of hosts to SSH into and submit jobs, or $PBS_NODE_FILE
```

# Usage
```
usage: scheduler.py [-h] [--hostfile HOSTFILE] [--cpu CPU] [--mem MEM]
                    [--log LOG]
                    jobsfile
```
