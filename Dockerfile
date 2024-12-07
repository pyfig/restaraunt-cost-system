FROM ubuntu:20.04 as builder

FROM python:3.10.7

RUN apt-get update && \
      apt-get -y install sudo

RUN useradd -ms /bin/bash docker && echo "docker:docker" | chpasswd && adduser docker sudo

RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER docker

USER root

WORKDIR /home/docker
COPY src/build* .

RUN sudo apt-get install apt-utils
RUN sudo apt-get update && apt-get install -y \
    python3-pil \
    python3-tk \
    python3-pil.imagetk

RUN pip install --upgrade pip
    
RUN mkdir /.local; mkdir /.local/share; chmod 777 /.local; chmod 777 /.local/share

ENV DISPLAY=unix$DISPLAY

CMD ["python3", "gui.py"]