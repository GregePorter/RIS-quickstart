This repository contains all the information you need to get started running Python and Jupyter Lab on the CPUs and GPUs available on WashU's RIS Cluster

## Task 1: Getting Access

First, you will need to get access to the RIS Cluster. Each faculty gets 5TB of free storage on the RIS Storage Cluster and access to open CPUs and GPUs on the Compute Cluster. If you're a student, you will simply be assigned access to your advisor's resources. To request access, submit a ticket at https://ris.wustl.edu/support/service-desk/. This process will probably take a few days, and you'll need your advisor to oversee the process.

## Task 2: Connecting to the RIS

To access the RIS cluster, you will need to perform the following steps.

1. If you are off-campus, you will need to be on the WashU VPN. Instructions on how to do so can be found at https://it.wustl.edu/items/connect/.
2. You should open a terminal on your computer, and SSH into the compute environment with the command `ssh <wustl-key>@compute1-client-<N>.ris.wustl.edu` where `<key>` is your official WUSTL key, and `<N>` can be any number from 1 to 4
   - e.g. `g.porter@compute1-client-4.ris.wustl.edu`
   - It should be noted that despite being called `compute1`, this is a "login" node, not a "compute" node. This means that you should not run any complicated code, you should instead use a "compute" node to run your code, using the steps either in Task 3, Task 11, or Task 12.

## Task 3: Installing Globus

## Task 4: Running a basic non-interactive job

## Task 5: Running a basic interactive job

## Task 6: How Docker Works

## Task 7: Making a custom Docker container

### Helpful commands if your job is stuck or exiting early

If your job is stuck without landing, or your job lands and immediatly deletes itself, here are some commands you can try.

1. SSH into the login node with `ssh <wustl-key>@compute1-client-<N>.ris.wustl.edu`
2. Use `bjobs -wa` to show all of your current and recent jobs
3. If your job hasn't landed yet (still grey), then run `bjobs -l <job-id>`, which will give you a reason for why your job hasn't landed yet
4. If your job has landed but is still blue after more than 10-15 minutes of waiting, then you can run `bpeek <job-id>` to view the current status of the job.
5. If your job exits right away, your job is crashing for some reason. You should run `cd ondemand/data/sys/dashboard/batch_connect/sys/jupyter/output/`, use `ls -lh` to find the most recently created folder, and `cd` into that folder. You can then view the output with `cat output.log` (or use `less output.log` if your file is really long. Exit `less` by typing in the letter `q`)
   - One common scenario why jobs might crash immediately is because storage1 is not set up correctly. If you try leaving the `Mounts` parameter empty and your new job doesn't crash, it means your RIS Storage hasn't been set up. Submit a ticket on RIS
6. `bhosts -w -gpu general-interactive` can be used to see what GPU's are available to a given queue. The queue in this case is `general-interactive` 

## Task 3: Run your first Jupyter Notebook

Running code in Jupyter is almost as easy.

1. First, you should open the `task-05.ipynb` file, by double clicking on it in the file browser.
2. By default, the notebook will try to open in the `base` conda kernel. However, I'm currently encountering a bug and this kernel doesn't load. To fix this, you can click on the `base` or `No Kernel` button at the top left of the screen, and instead select the `Python 3` kernel. The choice of which kernel you use determines which Conda environment your code runs with. We'll explain more about this in the next step.
3. Then, you can run your code by clicking the `Run → Run All Cells` button in the menu options.
4. Once the code finishes running, you can view the output saved to `02-output.txt`.
5. You can instead edit the code to save output file in RIS Storage instead of your home directory.

## Task 11: Submitting Python Jobs to the Cluster

Sometimes, you will want to run the same Python script with many different parameters. You could do this inside Jupyter Lab, but this could get cumbersome if you have hundreds or thousands of parameters you want to run. Instead, we can submit this Python script as a seperate _job_ on the RIS cluster. This will allow us to easily manage multiple parameters, and allow us potentially use more resources, simultaneously, allowing us to finish running our code faster

As an example, we will demonstrate how to submit the `task-11.py` script as seperate jobs, so we can run run the code simultanously, with different parameters. If you take a look inside the `task-11.py` file, you will see that this script takes in a single parameter, `shape`, creates a random matrix in Pytorch with that shape, loads the matrix on either the CPU or GPU depending on availability, performs a number of matrix operations on it, saves the matrix to our RIS Storage, and prints the runtime.

Here are the steps for how to submit `task-11.py` as jobs.

1. Open the `task-11.py` script and edit the script to point to the correct RIS Storage path
   - Takes in a single parameter, `shape`
   - Creates a random matrix in Pytorch with that shape
   - Loads the matrix on either the CPU or GPU depending on availability
   - Performs 100 matrix operations on it
   - Times how long the operations takes
   - Saves the matrix to our RIS storage (make sure to edit the `output_folder` parameter)
2. Open the `task-11-gpu.sh` file, and edit the parameters to point to the correct RIS Storage path and use your correct `<wustl-key>`
   - You should also read the comments to understand what each of the other parameters represent
3. Run `mkdir -p /storage1/fs1/<faculty-id>/Active/quickstart/job_output`, as the `-o` parameter in `task-11-gpu.sh` requires this directory to exist.
4. Run `bgadd -L 100 /<wustl-key>/limit100`. This will create a new fair share allocation group for you so you can run up to 100 jobs simultaneously.
   - Don't misuse this, or RIS can remove your access to the Compute Cluster
5. In your terminal, run the command `unset LSF_DOCKER_PORTS`. Otherwise, you will not be able to submit the jobs.
6. Finally, you can submit the jobs with `bash task-11-gpu.sh`
   - Random note, submitting these jobs may create a file in your `RIS-quickstart` directory called `lib_check`, containing the ominous sounding text `Die will Fire...`. I don't know what this file does, or what it means, but I don't think it's a problem.
7. While your jobs are running, you can use the command `bjobs -w | sort` to view all the jobs you've created, and their status (if it's pending or running)
8. Once your job is running, you can view the current output with `bpeek <job-id>`. This command will not work once your job finishes
9. When your jobs finish, you will get an email with a summary of your job and some statistics.
10. To view the output of your jobs, enter the job output directory with `cd /storage1/fs1/<faculty-id>/Active/quickstart/job_output`. You can then see the names of all the files in this directory with the `ls -lh` command. You can then view a specific job's output with the command `cat <file-name>`
11. We can then view the data created by these commands by going to `cd /storage1/fs1/<faculty-id>/Active/quickstart/data_processed/gpu` and typing in `ls -lh`. The actual data is not in a human-readable format, but you can at least see how large each file is.
    - What do you notice about the file sizes?
12. Next, we can try doing the same process, but submitting our code as CPU-only rather than running our code on a GPU. First, open the `task-11-cpu.sh` file, and edit the parameters as needed
13. Then, run the script with `bash task-11-cpu.sh` (making sure to go back to the `RIS-quickstart` directory first with `cd ~/RIS-quickstart`)
14. Once the jobs are done, you can view the data output at `/storage1/fs1/<faculty-id>/Active/quickstart/data_processed/cpu`
    - Are the file sizes different with the gpu-created files? Why or why not?
15. You can also view the job outputs at `/storage1/fs1/<faculty-id>/Active/quickstart/job_output`
    - What do you notice about the runtimes for each file?
    - Hint, try running `ls -v * | xargs -I{} grep -H "Function Runtime" {} | awk -F: '{printf "%-25s %s\n", $1":", $2":"$3}'`

## Task 12: Using Docker instead of Open OnDemand

At times, you may encounter a scenario where Open OnDemand doesn't work for your code. Maybe you need a different operating system instead of Ubuntu, or you need additional terminal commands such as `sudo`, or you need additional features in Jupyter such as Tensorboard or the NVIDIA GPU Dashboards. If any of these is true, you won't be able to use Open OnDemand, you'll have to build your own Docker image and run code for that.

In this section, I'm going to be a little more brief with my instructions, and I'm assuming that anybody that needs to build a Docker container is already proficient with the command line. As always, if you have any questions, you should consult the RIS Documentation or submit a ticket with the RIS Service Desk.

1. Create an account on [Docker Hub](hub.docker.com)
2. Create a new public repository on Docker Hub, named `<container-name>`
3. Download the Docker Desktop app on your personal computer and sign into your account
4. Download the `Dockerfile` and `docker-environment.yml` files from this Github repo onto your personal computer
5. Customize the `Dockerfile` with whatever requirmenets you need for your setup. The file I've provided is the simplest possible `Dockerfile` which will work on the RIS Cluster, but you can make any additional changes you need.
6. If you want, you can customize the `docker-environment.yml` with additional packages. In general, I would try to keep this environment as minimal as possible, and use the approach described in Task 6 to define custom conda environments for each project. If you need to install additional Jupyter extensions, you will need to do it here, rather than in your project-specific environment configs.
7. Build your Docker container with `docker build -t <docker-id>/<container-name>:<optional-tag>`, where `<docker-id>` is your username on Docker Hub, and `<container-name>` is the name of the public repository you created. Each repository can store multiple versions of a container, and each of these are distinguished by their `<tag>`.
8. Push your Docker container to Docker Hub with `docker push <docker-id>/<container-name>:<optional-tag>`. Depending on the size of your container, this could take anywhere from several minutes to several hours.
9. Log into the compute cluster with `ssh <wustl-key>@compute1-client-<N>.ris.wustl.edu`
   - This will bring you to one of the RIS login nodes. This is essentially a server where you can launch and view jobs which run your code. However, the login node isn't intended as a computer to run intensive code directly, so you'll have to learn how to submit jobs.
10. Download the `jupyter-gpu.sh` file from this Github repo
    - If you don't need to request a Jupyter Lab instance with a GPU, use `jupyter-cpu.sh` instead
11. Edit the `jupyter-gpu.sh` command to refer to your advisor's `<faculty-id>`
12. Launch a new Jupyter Lab instance by running the script `bash RIS-quickstart/jupyter-gpu.sh` with whatever parameters you want to customize.
    - For example, if you want to launch a job with 100GB of memory, a time limit of 24 hours, and 8 CPUs, you would use `bash RIS-quickstart/jupyter-gpu.sh -m 100GB -t 24 -c 8`
    - If you don't need a GPU, you would use `bash RIS-quickstart/jupyter-cpu.sh -m 100GB -t 24 -c 8`
13. In order to check if your job has landed, use the `bjobs -w` command. Once your job lands, the job status will change from `PEND` to `RUN`
    - If your job is taking a really long time to land, you can use the `bjobs -l <job-id>` command to get a detailed description of your job, including the reason why it hasn't landed yet
    - I created a script called `cluster_status.py`, which allows you to view status of the cluster. You can run ith with `python3 cluster_status.py` (on the login nodes, Python 2 is still the default even though it's 2024). This script is very helpful to see how occupied the cluster is, and can tell you potentially why your jobs aren't landing, if there are open GPUs or CPUs, etc.
14. Once your job has landed, use the `bpeek <job-id>` command to view your Jupyter Notebook url, which will look something like `http://compute1-exec-207.ris.wustl.edu:8401/lab?token=<token>`
    - If your job output is too long, you can use `bpeek <job-id> | grep http` as a shorthand to find the url
    - There are a bunch of additional compute cluster commands which mostly all start with the letter b, and many of them are useful. You can read more about them at https://www.ibm.com/docs/en/spectrum-lsf/10.1.0?topic=started-quick-reference
15. Finally, you can access your Jupyter Lab instance by going to the given URL.
    - In order to access this url, you need to be on the WashU VPN - even if you're on campus and connected to WashU's network
    - The first time you access the instance, you will need to copy paste the entire URL, including the token.
    - Afterwards, you can drop the token, and just enter the shortened url (e.g. `http://compute1-exec-207.ris.wustl.edu:8401/lab`)

Now you're in! Until your job dies, you can continue to access this url to get to Jupyter. You can now continue with Tasks 4 through 11.
