# FROM ubuntu:latest
# FROM debian:jessie
# FROM brunneis/python:3.7.0-ubuntu-18.04
FROM python:3.7.13

# RUN apt install software-properties-common
# RUN add-apt-repository ppa:deadsnakes/ppa
# RUN apt update
# RUN apt install python3.7.4
# RUN apt-get update
# RUN apt-get install python3.7
# RUN apt-get update \
#   && apt-get install -y \
#   python-setuptools

# 0. Install essential packages
RUN apt-get update \
  && apt-get install -y \
  build-essential \
  #         cmake \
#         git \
  wget 
  # python3.7 \
  # python-pip \
  # python-dev \
  # python-setuptools \
  # libpq-dev
  #         unzip \
#         unixodbc-dev \
#     && rm -rf /var/lib/apt/lists/*

# 1. Install Chrome (root image is debian)
# See https://stackoverflow.com/questions/49132615/installing-chrome-in-docker-file
ARG CHROME_VERSION="google-chrome-stable"
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update -qqy \
  && apt-get -qqy install \
    ${CHROME_VERSION:-google-chrome-stable} \
  && rm /etc/apt/sources.list.d/google-chrome.list \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*


# 2. Copy code to image
COPY . /app

# RUN pip install --upgrade setuptools
# RUN pip install --upgrade pip

# 3. Install other packages in requirements.txt
RUN cd /app && \
    pip install -r requirements.txt

# 4. Change working directory
WORKDIR /app

# 5. Start Flask app
ENTRYPOINT python /app/app.py
