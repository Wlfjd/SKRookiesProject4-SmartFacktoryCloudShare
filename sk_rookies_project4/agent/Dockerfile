FROM python:3.7 AS builder
RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx

WORKDIR ./agent
COPY . agent/

RUN pip3 install -r ./agent/requirements.txt

ENV AWS_PROFILE default
ENV AWS_DEFAULT_REGION us-west-2


CMD ["python","agent"]
