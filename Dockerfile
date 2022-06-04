FROM ubuntu
WORKDIR /mcontracts

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Kiev

RUN apt update
RUN apt install -y software-properties-common curl
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install -y python3.9 python3.9-distutils

# Install pip
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.9

COPY requirements.txt .
RUN python3.9 -m pip install -r requirements.txt

COPY . .

RUN pybabel compile -d data/locales -D bot-loc

CMD [ "python3.9", "./app.py" ]
