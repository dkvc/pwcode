FROM python:latest

RUN useradd -ms /bin/bash dev
USER dev

WORKDIR /home/dev/

COPY dev-reqs.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

LABEL name="pwcode"
LABEL version="0.1.0"
