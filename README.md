This repository contains all the information you need to start running jobs on the CPUs and GPUs available on WashU's RIS Cluster.

# Task 1: Getting Access

First, you will need to get access to the RIS Cluster. Each faculty gets 5TB of free storage on the RIS Storage Cluster and access to open CPUs and GPUs on the Compute Cluster. If you're a student, you will simply be assigned access to your advisor's resources. To request access, submit a ticket at https://ris.wustl.edu/support/service-desk/. This process will probably take a few days, and you'll need your advisor to oversee the process.

For the purposes of this workshop (if you are reading this during the workshop), you will have been given temporary access! For this temporary access, your storage location will be 

`/storage1/fs1/workshops/Active/HPCatWashU/`

and your queue and workgroup will be the following:
`-q workshop `
`-G compute-workshop`

We'll return to the queue and group later when we run jobs.

# Task 2: Connecting to the RIS

To access the RIS cluster, you must perform the following steps.

1. You should open a terminal on your computer, and SSH into the compute environment with the command `ssh <wustl-key>@compute1-client-<N>.ris.wustl.edu` where `<key>` is your official WUSTL key, and `<N>` can be any number from 1 to 4
   - e.g. `g.porter@compute1-client-4.ris.wustl.edu` or `g.porter@compute1-client-2.ris.wustl.edu`
2. You will be prompted for your password. Enter your Wustl Key password. Note, you won't see the characters as you type them. Also, note, you might be prompted to accept a security fingerprint - if you are, type `yes`.

If you are off-campus, you must be on the WashU VPN. Instructions on how to do so can be found at https://it.wustl.edu/items/connect/.

# Task 3: Installing Globus
Globus is the recommended method of transferring data and scripts to the RIS.
1. [Install Globus Connect Personal](https://docs.globus.org/globus-connect-personal/install/) - this will allow you to access your local files to then push to the RIS
2. Open the [Globus App](https://app.globus.org/)
3. Login with your Wustl Key
4. Once you're connected, look for the Storage1 collection
5. For this workshop, your storage1 location will be `/storage1/fs1/workshops/Active/HPCatWashU/` so use that as your path.
6. On your local machine, look for your local collections
7. Find the desired files, select them, and click Start to transfer them to the destination (the storage1 location)
8. We'll start by transferring [a Python script](https://github.com/GregePorter/RIS-quickstart/blob/ede971a3a88933ec91dc296a577ee683446073ec/basic-python.py) which can be found in this repository.

Note, the RIS has some [additional tutorials related to Globus](https://docs.ris.wustl.edu/doc/storage/globus.html)

## Exercise 1.1: Make a directory in the workshop's storage1 location
   When you've navigated to your destination in Globus, control + click (or right-click) some whitespace. You'll see a window popup. Select New Folder. Name it your name. This will be your directory for the rest of the workshot.
   
## Exercise 1.2: Transfer an R script
Transfer the [R script in this repository](https://github.com/GregePorter/RIS-quickstart/blob/ede971a3a88933ec91dc296a577ee683446073ec/basic-r.R) to your storage1 location

# Task 4: Running jobs

There are two main ways to run jobs on the RIS: non-interactive and interactive.

# Task 4.1: Running a basic non-interactive job
A non-interactive job means that you run the bsub command and you'll get a message that looks something like this:

`Job <876747> is submitted to queue <workshop>`

You'll get an email when the job finishes. This email will contain information about the job and all the text printed to the terminal.

To run a basic job,
1. SSH into the RIS
   
   `ssh g.porter@compute1-client-4.ris.wustl.edu` (where `g.porter` is replaced by your username)

2. Once here, we can run the `bsub` command to run the job but first we have to find it so `cd` into your storage location.
   
   `cd /storage1/fs1/workshops/Active/HPCatWashU/<your_username>` so mine would be

   `cd /storage1/fs1/workshops/Active/HPCatWashU/g.porter`
   
4. In our case, the script will be in our storage location. So the command with be
   
     `bsub -G compute-artsci -q artsci-interactive -a "docker(python:latest)" python basic-python.py`

Let's break down this command.
- `bsub` this allows a user to "submit a job for batched execution"
- `-G compute-artsci` specifies the Group that one is a member of (I'm part of `compute-artsci` and for, the purposes of this workshop, you will be part of `compute-workshop`)
- `-q artsci-interactive` specifies the Queue into which you will submit the job. `workshop` will be the Queue you use for the workshop.
- `-a "docker(python:latest)"` specifies which image you use. Let's break this down a little more too
   - `docker` means to go up to DockerHub (we'll talk more about this later)
   - `(python:` means to look for the [official Python container image on docker hub](https://hub.docker.com/_/python)
   - `:latest)"` tells docker to look for the Tag (or specific version of the `python` container image). There are a bunch of tags that refer to different versions (like `3.9.20` or `3.14.0a1-slim-bullseye`) which are all listed on Docker Hub.
- `python basic-python.py` this is the command that will run when the docker container starts. In a non-interactive job, this is the thing that runs and you'll see the output in the resultant email. We can open up the `basic-python.py` to understand what we should expect to see. 

# Task 4.2: Running a basic interactive job
An interactive job will not send you an email, instead, it will print everything to the terminal or allow you to type as if it were an ssh terminal (or python prompt). The key difference is the flag `-Is`.

Let's look at three examples.

### `python basic-python.py`

Just like with the non-interactive jobs, the last part of the command (`python basic-python.py`) is the command that will run when job starts.

If we run the following, the output of the script will printed to the terminal and, once the script ends, the job will end.

`bsub -Is -G compute-artsci -q artsci-interactive -a "docker(python:latest)" python basic-python.py`

### `python`
Now, for an actually interactive job, we can run the following to open up a python prompt

`bsub -Is -G compute-artsci -q artsci-interactive -a "docker(python:latest)" python`

### `/bin/bash`
Similarly, we can open up a regular bash terminal with the following

`bsub -Is -G compute-artsci -q artsci-interactive -a "docker(python:latest)" /bin/bash`

The command for running an interactive job is largely the same as a non-interactive job.

### Additional notes
Note, there is a time limit of 24 hours on interactive jobs so the only real reason to run an interactive job is for troubleshooting and last fine-tuning.

# Task 5: How Docker Works

A common question for Docker is "What is Docker and how does it compare to a virtual machine?"

A virtual machine requires the system to designate a portion of memory, hard drive space, and computing power to that machine. Docker doesn't lock that memory so it gives you a lot more flexibility.

[This is a little video that helped me better understand the components of Docker](https://www.youtube.com/watch?v=mxVkNGkzuxU).

# Task 7: Making a custom Docker container

Note, for this part, we'll need to have a DockerHub account.

So we have this notion of a base docker container like `r-base` or `python`. What happens if we want to do something with additional libraries like `bigmemory` or `numpy`? To do this, we would have to make our dockerfile, build it (locally or on the RIS), and upload it to Dockerhub.

We'll start with `Python` and then the exercise will be to do it with `R`
1. Let's open up the [Dockerfile-python in this repository](https://github.com/GregePorter/RIS-quickstart/blob/main/Dockerfile-python)
2. Once we have it downloaded, we have two options - build it locally and build it on the RIS.

### Building locally
If you have Docker installed locally, we'll build it from the terminal.

1. Open the Terminal
2. `cd` to the location of your Dockerfile
3. Run the docker build command
4. Run the docker run command to confirm it works
5. Tag the docker image container
6. Push it to DockerHub

### Building on the RIS
If you have an M1 Mac, you'll have to build on the RIS. 

1. Transfer the Dockerfile to your storage1 location on the RIS
2. `ssh` into the RIS
3. Run the docker build command
   This will tag and push the image to DockerHub


### Run the new Docker container
This process is the same as the earlier task. Instead of pointing the `bsub` command to `"docker(python:latest)"` we'll point it to you DockerHub account, image and tag.

# Task 8: Running batches of jobs
`https://docs.ris.wustl.edu/doc/compute/recipes/job-execution-examples.html?highlight=job%20array#arrays`
The scripts for this could be `output-file-r.R` and  `output-file-python.py`
The trick with this will be to name the file the name of the job id from the `bsub` command.

# Task 9: Making STORAGE, HOME, and other files available to the jobs
We can set environment variables using the following commands
```
export STORAGE=/storage1/fs1/workshops/Active/HPCatWashU
export HOME=/home/g.porter
export LSF_DOCKER_VOLUMES="$STORAGE:$STORAGE $HOME:$HOME"
```

Your jobs will then have `STORAGE` and `HOME` available to them. For Python, you can use the `os` library to access the environment variables. 
```
import os
print(os.environ['STORAGE'])
```

When you run an interactive job with that in the code, you'll see 

`/storage1/fs1/workshops/Active/HPCatWashU`

in the output.

### Helpful commands

If your job is stuck without landing, or your job lands and immediatly deletes itself, here are some commands you can try.

1. SSH into the login node with `ssh <wustl-key>@compute1-client-<N>.ris.wustl.edu`
2. Use `bjobs -wa` to show all of your current and recent jobs
3. If your job hasn't landed yet (still grey), then run `bjobs -l <job-id>`, which will give you a reason for why your job hasn't landed yet
4. If your job has landed but is still blue after more than 10-15 minutes of waiting, then you can run `bpeek <job-id>` to view the current status of the job.
6. `bhosts -w -gpu general-interactive` can be used to see what GPU's are available to a given queue. The queue in this case is `general-interactive` 
7. `Exited with exit code 137.` is the error message you get if your job ran out
   of memory.
8. You can view what groups you are a member in using the `groups` command.
9. And you can view all available queues using bqueues. If you want to see which queues you can access specifically, add the -u WUSTL_KEY_ID option.
     `bqueues -u g.porter` would be mine.

### Noteable documentation pages 
1. [Job examples](https://docs.ris.wustl.edu/doc/compute/recipes/job-execution-examples.html?highlight=span)
2. [Accessing storage from jobs](https://docs.ris.wustl.edu/doc/compute/recipes/ris-compute-storage-volumes.html?highlight=volume#normal-operations)
   2.1 - Once you've SSH'ed into the RIS, run `export STORAGEN=<path_to_your_storage1_folder>` so mine would be `export STORAGEN=/storage1/fs1/artsci/Active/g.porter`. For this workshop, you're would be something along the lines of `export STORAGE=/storage1/fs1/workshops/Active/HPCatWashU/`.
   2.2 - Then run the command export `LSF_DOCKER_VOLUMES="$STORAGE:$STORAGE"`
   2.3 - Once you run this, your home directory and your storage directory will be available in the docker container. So if you ran an interactive job, you could run `cd $STORAGE` and be taken to your storage directory.
