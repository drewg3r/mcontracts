FROM ubuntu
WORKDIR /mcontracts

RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install -y python3.9 python3-pip

COPY requirements.txt .
RUN python3.9 -m pip install -r requirements.txt

COPY . .

RUN pybabel compile -d data/locales -D bot-loc

CMD [ "python3.9", "./app.py" ]