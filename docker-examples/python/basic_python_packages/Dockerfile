#Start from bionic base Ubuntu image.
FROM ubuntu:20.04

#Update the base software inthe ubuntu image
#install python pip and libatlas-base-dev
#the flag -y is really important it means to not prompt anything in the console
RUN apt-get update \
    && apt-get install -y python pip libatlas-base-dev \
    && apt-get clean

#Once everything is installed use pip to install the modules below
RUN pip install python-dotenv pybind11 scipy python-config
