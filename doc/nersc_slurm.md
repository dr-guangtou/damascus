# Basics about Running Jobs using SLURM

---- 

## `Slurm`

- [`Slurm`](https://slurm.schedmd.com/overview.html) is an open source, fault-tolerant, and highly scalable cluster management and job scheduling system for large and small Linux clusters.

### Basic Commands

- [`srun`](https://slurm.schedmd.com/srun.html): submit a job for execution or initiate job steps in real time.
	- A job can contain multiple job steps executing sequentially or in parallel on independent or shared resources within the job's node allocation.
- [`sbatch`](https://slurm.schedmd.com/sbatch.html): submit a job script for later execution. The script will typically contain one or more srun commands to launch parallel tasks.
- `sacct`: report job or job step accounting information about active or completed jobs.
- [`salloc`](https://slurm.schedmd.com/salloc.html): allocate resources for a job in real time. 用于分配资源并生成shell。然后使用shell执行srun命令以启动并行任务。
- `sattach`: attach standard input, output, and error plus signal capabilities to a currently running job or job step.
- `sbcast`: transfer a file from local disk to local disk on the nodes allocated to a job
- `scancel`: cancel a pending or running job or job step.
- `sinfo`: reports the state of partitions and nodes managed by Slurm.
- [`squeue`](https://slurm.schedmd.com/squeue.html): reports the state of jobs or job steps. By default, it reports the running jobs in priority order and then the pending jobs in priority order.
- `sstat`: get information about the resources utilized by a running job or job step.
- `strigger`: set, get or view event triggers. Event triggers include things such as nodes going down or jobs approaching their time limit.

#### `sbatch` and script


### Reference

- [Man pages for `Slurm` commands](https://slurm.schedmd.com/man_index.html)
- [`Slurm` 快速达入门用户指南](https://docs.slurm.cn/users/kuai-su-ru-men-yong-hu-zhi-nan)
- [`Slurm` official documents](https://slurm.schedmd.com/documentation.html)
- [`Slurm` 作业调度系统使用指南 by 中国科大超级计算中心](http://hmli.ustc.edu.cn/doc/userguide/slurm-userguide.pdf)


## NERSC Clusters

### [Cori](https://docs.nersc.gov/systems/cori/)

- A Cray XC40 with a peak performance of about 30 petaflops. 
- Cori is comprised of 2,388 Intel Xeon "Haswell" processor nodes, 9,688 Intel Xeon Phi "Knight's Landing" (KNL) nodes.

### Useful notes

- Login nodes are for editing, compiling, preparing jobs, not for running jobs.
- Cori has [dedicated nodes for interactive work](https://docs.nersc.gov/jobs/interactive/).
	- For Cori Haswell: `salloc --qos=interactive -C haswell --time=60 --nodes=2`
	- For Cori KNL: `salloc --qos=interactive -C knl --time=60 --nodes=2`
- Submitting jobs using `srun`, `sbatch`:
	- At a minimum a job script must include **number of nodes, time, type of nodes (constraint), and quality of service (QOS)**. If a script does not specify any of these options then a default may be applied.
	- Default is 1 node, 10 mins, `qos=debug`.
	- It is good practice to always set the account option (`--account = <NERSC Repository>`).
	- In the script file, set `sbatch` option using something like `#SBATCH -N 2`
	- Multiple Parallel Jobs Sequentially: Multiple `sruns` can be executed one after another in a single batch script. Be sure to specify the total walltime needed to run all jobs.
	- [Multiple Parallel Jobs Simultaneously](https://docs.nersc.gov/jobs/examples/#multiple-parallel-jobs-simultaneously): use `&` at the end of `srun` command, and add `wait` at the end. 
- **Updating jobs**: `scontrol` command allows certain charactistics of a job to be updated while it is still queued. Once the job is running most changes will not be applied. e.g. `scontrol update jobid=$jobid timelimit=$new_timelimit`
	- Can also hold and release queued job: `scontrol hold/release JOBID`.
- **Quota enforcement**: Users will not be allowed to submit jobs if they are over quota in their scratch or home directories. This quota check is done twice, first when the job is submitted and again when the running job invokes srun.
	- [About checking quotas](https://docs.nersc.gov/filesystems/quotas/): `myquota` command.
- **Long running jobs**: Simulations which must run for a long period of time achieve the best throughput when composed of many small jobs utilizing checkpoint/restart chained together.
- [**Improve Efficiency by Preparing User Environment Before Running**](https://docs.nersc.gov/jobs/best-practices/#improve-efficiency-by-preparing-user-environment-before-running): should prepare the user environment on a login node, propagate this environment to a batch job, and submit the batch job.

- **Monitoring the job**:
	- `sacct -j JOBID`: report job or job step accounting information about active or completed jobs.
	- For users who are interested in monitoring their job's resource usage while the job is running, NERSC provides the `ssh_job JOBID` command.
	- `sqs` is used to view job information for jobs managed by Slurm.
	- Can use e-mail notification:

```
#SBATCH --mail-type=begin,end,fail
#SBATCH --mail-user=user@domain.com
```

- **Memory**: the available memory we set in Slurm for applications to use is **118 GB** on a Haswell node, and **87 GB** on a KNL node.
	- There are two nodes on Cori with 750 GB of memory that can be used for jobs that require very high memory per node. There are only two nodes, so this resource is limited and should only be used for jobs that require high memory.

- **MPI**
	- [Intel MPI](https://docs.nersc.gov/jobs/examples/#intel-mpi): Applications built with Intel MPI can be launched via `srun` in the Slurm batch script on Cori compute nodes. The module `impi` must be loaded.
	- [Open MPI](https://docs.nersc.gov/jobs/examples/#open-mpi): Applications built with Open MPI can be launched via `srun` or Open MPI's `mpirun` command. The module `openmpi` needs to be loaded to build an application against Open MPI.

- [Variable-time jobs](https://docs.nersc.gov/jobs/examples/#variable-time-jobs)
	- Variable-time jobs are for users who wish to get a better queue turnaround and/or need to run long running jobs, including jobs longer than 48 hours. 
	- Variable-time jobs are jobs submitted with a minimum time, `#SBATCH --time-min`, in addition to the maximum time (`#SBATCH –time`).

### File Systems

- [Community](https://docs.nersc.gov/filesystems/community/): 20TB, 20M inodes; Can't write new data once exceeding quota.
	- **CFS** (Community File System) allows sharing of data between users, systems, and the "outside world".
	- Imaging surveys are here: `/global/cfs/cdirs/cosmo/`
	- DESI related projects are here: `/global/cfs/cdirs/desi/`
- [Cori SCRATCH](https://docs.nersc.gov/filesystems/cori-scratch/): 20TB, 10M inodes; 12 weeks purge time; can't submit batch jobs once exceeding quota.
	- A Lustre file system designed for high performance temporary storage of large files. It is intended to support large I/O for jobs that are being actively computed on the Cori system.
	- `$SCRATCH`: is meant for large and temporary storage. It is optimized for read and write operations. It is perfect for staging data and performing parallel computations.
	- `$SCRATCH` = `/global/cscratch1/sd/YourUserName`
- [Global HOME](https://docs.nersc.gov/filesystems/global-home/): 40GB, 1M inodes; Can't write new data once exceeding quota.
	- Home directories (`$HOME`) provide a convenient means for a user to have access to files such as dotfiles, source files, input files, configuration files regardless of the platform. Global homes are backed up to HPSS monthly.
	- Performance of global homes is optimized for small files and is suitable for compiling and linking executables.
- [Global common](https://docs.nersc.gov/filesystems/global-common/): 10GB, 1M inodes; Can't write new data once exceeding quota.
	- It offers a performant platform to install software stacks and compile code.
	- Global common directories are created in `/global/common/software`
	- **Important**: Please note that while building software in /global/home is generally good, it is best to install dynamic libraries that are used on compute nodes in global common for best performance.

- When a quota is reached writes to that file system may fail.

### [Queue Policies](https://docs.nersc.gov/jobs/policy/)

- **Quality of Service** (QOS): each queue has a different service level in terms of priority, run and submit limits, walltime limits, node-count limits, and cost.
	- `regular`: 
		- Haswell: max nodes=1932; max time=48 hrs; submit limit=5000; priority=4
		- KNL: max nodes=9489; max time=48 hrs; submit limit=5000; priority=4
	- `debug`: is to be used for code development, testing, and debugging. 
		- **Important**: Don't use it for production run or your account will be suspended!
		- Haswell: max nodes=64; max time=0.5 hrs; submit limit=5; priority=3
		- KNL: max nodes=512; max time=0.5 hrs; submit limit=5; priority=3
	- `interactive`: is to be used for code development, testing, and debugging in an interactive batch session.
		- Jobs should be submitted via `salloc -q interactive` along with other salloc flags
	- `low`: allow non-urgent jobs to run with a lower usage charge.
	- `premium`: to allow for faster turnaround before conferences and urgent project deadlines. It should be used with care.
	- `flex`: to encourage user jobs that can produce useful work with a relatively short amount of run time before terminating. Only available on Cori KNL.

### Tools

- [NERSC Jobscript Generator](https://my.nersc.gov/script_generator.php)

### Reference

- [NERSC Technical Documentation](https://docs.nersc.gov/)
- [Example Job Scripts](https://docs.nersc.gov/jobs/examples/)
- [Running Jobs at NERSC](https://docs.nersc.gov/jobs/)
- [Best Practices for Jobs at NERSC](https://docs.nersc.gov/jobs/best-practices/)
- [Slurm Access to the Cori GPU nodes](https://docs-dev.nersc.gov/cgpu/access/)
- [Running Jobs on Cori with SLURM](https://www.nersc.gov/assets/Uploads/CoriP1-20160614-RunningJobs.pdf)
- [Running jobs at NERSC (Cori, Edison)](https://www.nersc.gov/assets/Uploads/04-Running-Jobs.pdf)


### NERSC User Environment

- NERSC won't populate dotfiles for you, you need to create your own `.bashrc` or `.bash_profile` file.
- On Cori `~/.bash_profile` and `~/.profile` are sourced by login shells, while `~/.bashrc` is sourced by most of the shell invocations including the login shells.
- **Important**: If you run `shifter` applications, you may want to skip the dotfiles. You can use the following if block in your dotfiles: 

```
if [ -z "$SHIFTER_RUNTIME" ]; then
    : # Settings for when *not* in shifter
fi
```

#### `module`

- NERSC uses the [`module`](https://modules.readthedocs.io/en/latest/) utility to manage nearly all software.
- `module list`: list currently loaded modules.
- `module avail <module-name>`: list available modules,
- `module load <module-name>`: add a module to your current environment.
- `module unload <module-name>`: remove module from the current environment.
- `module swap <old-module> <new-module>`: switch currently loaded module with a new module.

### Applications

#### Potentially Useful Modules

- There are different versions of these. Use `module load` to search for the one you need.
- Languages: `R`, `Python`, `go`, `IDL`, `mathematica`, `matlab`
- Editor: `emacs`, `texlive`, `vim`
- Astro-related: `cfitsio/3.47`, `ds9`, `dust`
- DESI-related: `desimodel`, `desimodules`, `desisim`, `desispec`, `desitarget`, `desisurvey`, `desitree`, `desiutil`, `fiberassign`, `redrock`, `specsim`, `specex`, `surveysim`
- Compilers and related: `gcc`, `gdb`, `glib`, `cmake`, `gsl`, `impi`, `intel`, `llvm`, `mpich`, `openmpi`, `swig`
- Version control: `git` and `git-lfs`, `subversion`
- Machine learning: `pytortch`, `tensorflow`
- `cuda`, `eigen3`, `boost`, `fftw`, `hdf`, `hdf5-parallel`, `opencv`
- `cray-fftw`, `cray-hdf5`, `cray-mpich`, `esslurm`, `zsh`

#### Using [Python](https://docs.nersc.gov/programming/high-level-environments/python/)

- At NERSC there are two major ways of using Python:
	- Default Python modules: `module load python`
		- Default Python for DESI member: `/global/common/software/desi/cori/desiconda`
	- The `conda` tool lets you build your own custom Python installation through "environments". You might do this if you need a library that is not in our default modules or require a custom setup.
		- e.g. `conda create -n myenv python=3 numpy`
		- Once you have created a conda environment, you have two options for activating it: `source activate` and `conda activate`.
		- `source activate` is the older, less invasive way to activate a conda environment. It will not make any changes to your shell resource files/dotfiles

- **Important**: Setting `PYTHONPATH` not advised

- Installing Python packages:
	- `conda search` and `conda install`: You can find packages and install them into your own environments easily.
		- If conda search fails to identify your desired package it may still be installed via `pip`.
	- `pip` install needs `--user` option: e.g. `pip install myfavoritepackage --user`; Although you don't need `--user` in your own conda environment. It is **important** to think carefully about which kind of environment you are in before you type.
		- It is good practice to use `pip install myfavoritepackage --user --no-cache-dirs`
	- The best-performing shared file system for launching parallel Python applications is `/global/common`

- Parallel computing in Python:
	- [Python multiprocessing](https://docs.nersc.gov/programming/high-level-environments/python/multiprocessing/) to achieve some level of parallelism within a single compute node.
		- If you are using the multiprocessing module, it is advised that you tell srun to use all the threads available on the node with the "-c" argument. For example, on Cori use: `srun -n 1 -c 64 python script-using-multiprocessing.py`.
		- **Important** Think carefully before using multiprocessing in Python: Python multiprocessing's shared memory model interacting poorly with many MPI implementations, threaded libraries, and libraries using shared memory.
	- To achieve parallelism across compute nodes [using `mpi4py`](https://docs.nersc.gov/programming/high-level-environments/python/mpi4py/)
		- The `mpi4py` library provides bindings for using MPI in Python. It can be used on a single node and all the way up to thousands of nodes.
		- **A word of caution**: using `mpi4py` on many nodes (~100+) can be very slow to start up. For larger `mpi4py` jobs we strongly recommend `Shifter` to help improve startup time.
	- [`Dask`](https://docs.nersc.gov/analytics/dask/) is a task framework that allows Python to flexibly scale from small to large systems.
	- **Important**: `import` in Python can take a lot of times! When a large number of Python tasks are running simultaneously, especially if they are launched with MPI, the result is many tasks trying to open the same files at the same time, causing contention and degradation of performance.	
		- On NERSC: build a Docker image containing their Python stack and use `Shifter` to run it.

- Your conda environment can easily become a Jupyter kernel. If you would like to use your custom environment `myenv` in Jupyter
	- Then when you log into `jupyter.nersc.gov` you should see `MyEnv` listed as a kernel option.

- [About profiling Python](https://docs.nersc.gov/programming/high-level-environments/python/profiling-python/)
	- `cProfile` + [`SnakeViz`](https://jiffyclub.github.io/snakeviz/) for profiling and visulization.
- [About running Python on Cori KNL](https://docs.nersc.gov/programming/high-level-environments/python/python-on-cori-knl/)
- [About using `h5py`](https://docs.nersc.gov/programming/libraries/hdf5/#h5py)


#### [Using `Jupyter` at NERSC](https://docs.nersc.gov/services/jupyter/)

- At NERSC, you can have access to [`JupyterHub`](https://jupyterhub.readthedocs.io/en/stable/) using your NERSC credentials and one-time password. The service is [here](https://jupyter.nersc.gov/).
	- `JupyterLab` is new but ready for use now. With release 0.33 we have made `JupyterLab` the default interface to Jupyter on both hubs.

- On Cori: Spawns Jupyter notebooks on special-purpose large-memory nodes.
	- Exposes GPFS and Cori `$SCRATCH`.
	- **Important**: Notebooks can submit jobs to Cori batch queues via simple Slurm Magic commands
	- **Important**: The nodes used by `https://jupyter.nersc.gov/` are a shared resource, so please be careful not to use too many CPUs or too much memory.

- `Shifter` Kernels on Jupyter (only Cori). To make use of it, create a kernel spec and edit it to run shifter. The path to Python in your image should be used as the executable, and the kernel spec should be placed at `~/.local/share/jupyter/kernels/<my-shifter-kernel>/kernel.json`.
