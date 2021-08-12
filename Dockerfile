FROM ubuntu
WORKDIR /mcontracts

RUN apt update
RUN apt install -y python3 python3-pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "./app.py" ]