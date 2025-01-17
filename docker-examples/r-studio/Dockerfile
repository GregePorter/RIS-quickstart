FROM gcr.io/ris-registry-shared/rstudio:3.6.3

# install packages using apt-get

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update --fix-missing && \
apt-get install -y build-essential \
libcurl4-gnutls-dev libxml2-dev \
libssl-dev && \
apt-get clean

# extend image to include tidyverse and devtools R packages

RUN R -e "install.packages(c('devtools','tidyverse','doMC','doParallel'), dependencies=TRUE, repos='https://cran.rstudio.com')"
