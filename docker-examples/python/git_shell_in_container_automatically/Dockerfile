#Start from bionic base Ubuntu image.
FROM ubuntu:20.04

#Copy all the files (by using a regular expression) from the current directory
#into the folder called copied_code which will be in the root of the project
COPY --chmod=775 * /copied_code/

#Clone the repo below and put it in the root directory of the container
#Note, you don't have to install git if you use ADD
#If you want to run a git command, you'll have to manually install git
ADD http://github.com/GregePorter/RIS-quickstart.git .

RUN apt-get update \
    && apt-get install -y python pip libatlas-base-dev \
    && apt-get clean

RUN pip install python-dotenv python-config

# run the following command when building the image
#RUN ./included_code/run_python.sh
