from python:3.7.4-alpine3.9 as builder

RUN mkdir /tmp/

WORKDIR /install

COPY requirements.txt /tmp/requirements.txt

RUN pip3.7 install --no-cache-dir -r /requirements.txt 

RUN adduser -D -g '' appuser

WORKDIR /home/appuser

USER appuser

COPY src/* .

CMD ["irc3", "-v", "-r", "/etc/t2t-daemon/config.ini"]

