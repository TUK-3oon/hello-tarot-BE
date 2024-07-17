FROM ubuntu:22.04

ENV TZ=UTC

RUN apt-get update && \
    apt install -y python3.10 python3-pip python3.10-distutils python3.10-dev libpq-dev && \
    ln -snf /usr/share/zoneinfo/UTC /etc/localtime && echo $TZ > /etc/timezone && \
    apt-get update && \
    apt-get install -y tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN ln -s /usr/bin/python3.10 /usr/bin/python

EXPOSE 8000

CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
