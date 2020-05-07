# Using Docker and Shifter at NERSC

----

## Docker

- `Docker` is a platform for developers and sysadmins to build, run, and share applications with containers.
	- Fundamentally, a container is nothing but a running process
	- One of the most important aspects of container isolation is that each container interacts with its own private filesystem; this filesystem is provided by a `Docker` **image**.
	- Docker is a tool that allows developers, sys-admins etc. to easily deploy their applications in a sandbox (called containers) to run on the host operating system.
	- It allows users to package an application with **all of its dependencies into a standardized unit**.

### Terminology

- `image`: The blueprints of our application which form the basis of containers.
- `container`: Created from Docker images and run the actual application.

### Basic tutorial

- [Getting started by Docker](https://docs.docker.com/get-started/)
- [Docker for beginner](https://docker-curriculum.com/)

### Basic commands

- `docker version` and `docker info` for basic information.
- `docker image ls`: list all the downloaded container.
- `docker search`: search for a container.
- `docker ps`: show the image that is currently running. With `-a`, it shows all the containers run before.
- `docker pull`: fetches the image from the Docker registry and saves it to our system.
- `docker run`: loads up the container and then runs a command in that container.
	- `docker run -it`: attaches us to an interactive tty in the container so can run many commands.
- `docker build --tag TAGNAME .`: build docker image using the current folder.
	- Then you can run your image as a container, `docker run --detach --name NICKNAME TAGNAME`.
		- If you need a port, use `-p 8888:5000`.
	- Once you tested the image, you can delete it using `docker rm --force NICKNAME`.
- `docker login`, `docker tag TAGNAME REPONAME` & `docker push REPONAME` can push your image to DockerHub.
	- For example, on how to [build a Docker container for use with Shifter at NERSC](https://github.com/legacysurvey/legacypipe/tree/DR9.3.4/docker-nersc)

### `Dockerfile`:

#### Reference: 

- [Reference for Dockerfile](https://docs.docker.com/engine/reference/builder/)
- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

- Dockerfiles describe how to assemble a private filesystem for a container, and can also contain some metadata describing how to run a container based on this image. Writing a Dockerfile is the first step to containerizing an application.
	- A step-by-step recipe on how to build up your image.

#### Example:

- [Dockerfile for `legacypipe` DR9](https://github.com/legacysurvey/legacypipe/blob/DR9.3.4/docker/Dockerfile)

#### Key Elements:

- `MAINTAINER`: Name of the mainainer.
- `FROM`: star from any pre-existing image.
- `WORKDIR`: specify that all subsequent actions should be taken from a directory in the **image**.
- `COPY`: copy the file from your host to your current location
- `RUN`: run the command inside your image filesystem.
- `CMD`: run the specified command within the container.
- `EXPOSE`: inform Docker that the container is listening on the specified port at runtime.
EXPOSE 8080
- `ADD`: similar to `COPY`. But there is a [difference](https://nickjanetakis.com/blog/docker-tip-2-the-difference-between-copy-and-add-in-a-dockerile).
- `ARG`: defines a variable that users can pass at build-time to the builder.
- `ENV`: sets the environment variable. [Difference between ARG and ENV](https://vsupalov.com/docker-arg-env-variable-guide/#setting-arg-values).

----

## `Shifter`

- [Using `Shifter` at NERSC](https://docs.nersc.gov/programming/shifter/how-to-use/)
	- [`Shifter`](https://github.com/NERSC/shifter) is a software package that allows user-created images to run at NERSC. Can be Docker images. 
	- `Shifter` also comes with improvements in performance, especially for shared libraries. It is currently the best performing option for python code stacks across multiple nodes.
	- `Shifter` can leverage its volume mounting capabilities to provide local-disk like functionality and IO performance.
	- `Shifter` can be used interacitvely on logins nodes or in a batch job.
	- `Shifter` has the ability to automatically allow communication between nodes using the high-speed Aries network.

- [Example Dockerfiles for Shifter](https://docs.nersc.gov/programming/shifter/examples/)
	- [Dark Energy Spectroscopic Instrument (DESI) experiment software stack](https://hub.docker.com/r/mmustafa/desi/tags/)
	- [Legacy Surveys data reduction / catalog generation pipeline](https://hub.docker.com/r/legacysurvey/legacypipe)
	- [LSST Operations Simulator](https://hub.docker.com/r/lsst/opsim4)

### Reference

- [Shifter-Tutorial - Collection of tutorials for using Shifter to bring containers to HPC](https://github.com/NERSC/Shifter-Tutorial)
- [Docker functionality with Shifter using SLURM](https://slurm.schedmd.com/SLUG15/shifter.pdf)

### Building `Shifter` Images

- Easiest way: build a Docker image on your computer or on the login node, upload it to DockerHub, then pull the image down to Docker friendly computer at NERSC (e.g. Cori).
	- `Shifter` images have a naming scheme that follows `source:image_name:image_version`.

### Gotcha

- [Using NERSC's Intel Docker Containers](https://docs.nersc.gov/programming/shifter/intel/)
- The software should be installed in a way that is executable to someone with user-level permissions.
	- To test: `docker run -it --user 500 <image_name> /bin/bash`
- Images are mounted read-only at NERSC, so software should be configured to output to NERSC file systems, like `$SCRATCH` or `Community`.
	- `Community` must be accessed in a shifter image by using its full path `/global/cfs/`.
- We have observed that programs built with `CMAKE` may override the use of the `LD_LIBRARY_PATH`. You can use `CMAKE_SKIP_RPATH` to disable this behavior.
- You will need to make sure any libraries installed in the image are in the standard search path. We recommend running an `/sbin/ldconfig` as part of the image build (e.g. in the Dockerfile) to update the cache after installing any new libraries in in the image build.

### Downloading Shifter Images To NERSC

- Download a public docker repositories: `shifterimg -v pull docker:image_name:latest`.
- To see a list of all available images: `shifterimg images`.

### Running Jobs in Shifter Images

- Submit job: `sbatch <your_shifter_job_script_name.sh>`.
- Example job script (This will invoke 32 instances of your image and run the `myPythonScript.py` in each one):

```
#!/bin/bash
#SBATCH --image=docker:image_name:latest
#SBATCH --nodes=1
#SBATCH --qos=regular
#SBATCH --constraint=haswell

srun -n 32 shifter python3 myPythonScript.py args
``` 

- For shared or single-core jobs:

```
#!/bin/bash
#SBATCH --image=docker:image_name:latest
#SBATCH --qos=shared
#SBATCH --constraint=haswell

shifter python3 myPythonScript.py args
```

### Volume Mounting

- Existing directories can be mounted inside a Shifter image using a `#SBATCH --volume directory_to_be_mounted:targer_directory_in_image` flag.
	- This allows you to potentially run an image at multiple sites and direct the output to the best file system without modifying the code in the image.

### Using MPI

- Just compile your image against the standard MPICH libraries and the Cray libraries will be swapped into the image at run time.
- Currently this functionality is only available for images where MPICH is installed manually (i.e. not with `apt-get install mpich-dev`)
- `Shifter` has functionality that can be toggled on or off using modules flags. Modules can be used together.
	- `#SBATCH --module=[mpich|mpich-cle6|cvmfs|none]`

- Example to run on two nodes:

```
#!/bin/bash
#SBATCH --image=docker:image_name:latest
#SBATCH --qos=regular
#SBATCH -N 2
#SBATCH -C haswell

srun -n 64 shifter python3 ~/hello.py
```