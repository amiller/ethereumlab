FROM ubuntu:14.04

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -qy software-properties-common curl git python2.7 python-pip python-dev libssl-dev libffi-dev pkg-config autoconf libtool

RUN add-apt-repository -y ppa:ethereum/ethereum
RUN apt-get update
RUN apt-get install -qy solc

RUN git clone --depth=1 --branch develop https://github.com/ethereum/serpent.git && cd serpent && python setup.py install
RUN git clone --depth=1 --branch develop https://github.com/ethereum/pyethereum.git && cd pyethereum && python setup.py install
RUN git clone --branch ece598fall2016 https://github.com/amiller/ethereumlab
