FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt


COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]