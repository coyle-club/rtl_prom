FROM docker.io/python:3.10.4-slim

COPY rtl_prom /app/rtl_prom

COPY setup.py /app/setup.py

RUN pip install -e /app

ENTRYPOINT ["/usr/local/bin/rtl_prom"]







