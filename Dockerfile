from python:3.7.4 as base

COPY requirements.txt /tmp/requirements.txt

RUN pip3.7 wheel --no-cache-dir --no-deps --wheel-dir /wheels -r /tmp/requirements.txt 

FROM python:3.7.3-slim

RUN useradd -ms /bin/bash appuser

WORKDIR /app

COPY --from=base /wheels /wheels

RUN pip3.7 install --no-cache-dir /wheels/*

USER appuser

COPY src/ .

CMD ["irc3", "-v", "-r", "config.ini"]

