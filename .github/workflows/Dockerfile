FROM ubuntu:latest

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

RUN python3 get-pip.py && rm get-pip.py

ADD eo-catalog /app/eo-catalog
RUN pip install --no-cache-dir /app/eo-catalog && rm -rf /app

RUN pip cache purge
