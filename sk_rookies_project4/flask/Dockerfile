# docker build --no-cache -t was:1.0 ./flask
# docker run -itd --name was -v ~/.aws/:/root/.aws:ro --env AWS_PROFILE=default was:1.0 

FROM python:3.7 AS builder
RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx


WORKDIR ./flask
COPY . flask/

RUN pip install -r ./flask/requirements.txt

ENV FLASK_APP run.py
ENV FLASK_DEBUG True
ENV FLASK_RUN_PORT 8000
ENV FLASK_RUN_HOST 0.0.0.0

ENV AWS_PROFILE default
ENV AWS_DEFAULT_REGION us-west-2

EXPOSE 8000
 
WORKDIR ./flask

CMD ["flask", "run"]


