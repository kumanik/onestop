# Base Image
FROM ubuntu:18.04 as base

# set working directory
WORKDIR /usr/src/

# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    libopencv-dev \ 
    build-essential \
    libssl-dev \
    libpq-dev \
    libcurl4-gnutls-dev \
    libexpat1-dev \
    gettext \
    unzip \
    python3-setuptools \
    python3-pip \
    python3-dev \
    python3-venv \
    git \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install environment dependencies
RUN pip3 install --upgrade pip numpy
RUN pip3 install --no-use-pep517 pandas
COPY ./requirements.txt /usr/src/requirements.txt
RUN pip install --no-use-pep517 -r requirements.txt

# copy project to working dir
COPY . /usr/src/

# RUN python3 manage.py makemigrations
# RUN python3 manage.py migrate
# RUN python3 manage.py runserver 0.0.0.0:8000