FROM python:3-slim

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      build-essential \
      gcc \
      i2c-tools \
      libjpeg62-turbo \
      libopenjp2-7 \
      zlib1g \
      libfreetype6 \
      procps \
      iproute2 \
      zlib1g-dev \
      swig \
      git \
      python3-dev \
      libjpeg-dev \
      wget ca-certificates && \
    rm -rf /var/lib/apt/lists/*


RUN git clone https://github.com/joan2937/lg \
    /tmp/lg \
    && cd /tmp/lg \
    && make \
    && make install \
    && ldconfig

RUN pip install --upgrade pip setuptools wheel

RUN pip install --no-cache-dir \
      adafruit-blinka \
      adafruit-circuitpython-ssd1306 \
      pillow \
      RPi.GPIO \
      gpiozero \
      smbus \
      psutil \
      lgpio

WORKDIR /opt/stats

COPY *.py *.ttf .

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python"]
CMD ["stats.py"]
