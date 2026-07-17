#!/usr/bin/env python3

import os
import sys
import time
import atexit
import signal
import socket
import docker
from docker.errors import DockerException

import board
import digitalio
import adafruit_ssd1306

from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 128, 32
FONT_SZ = 12


oled = adafruit_ssd1306.SSD1306_I2C(
    WIDTH,
    HEIGHT,
    board.I2C(),
    addr=0x3C,
    reset=None
)

rotation = int(os.environ.get("OLED_ROTATION", "1"))
if rotation == 2:
    try:
        oled.rotate(2)
    except AttributeError:
        oled.rotation = 2

try:
    docker_client = docker.DockerClient(base_url="unix:///var/run/docker.sock")
    # Test the connection once at startup
    docker_client.ping()
except DockerException:
    docker_client = None

def cleanup():
    try:
        oled.fill(0)
        oled.show()
    except Exception:
        pass


atexit.register(cleanup)


def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "0.0.0.0"


def get_docker_count():
    if docker_client is None:
        return 0

    try:
        return len(docker_client.containers.list())
    except DockerException:
        return 0


image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# font = ImageFont.truetype("PixelOperator.ttf", FONT_SZ)
font = ImageFont.load_default()

last_frame = None

while True:
    ip = get_ip()
    containers = get_docker_count()

    frame = (ip, containers)

    if frame != last_frame:
        draw.rectangle(
            (0, 0, oled.width, oled.height),
            fill=0
        )

        draw.text(
            (0, 0),
            f"IP: {ip}",
            font=font,
            fill=255
        )

        draw.text(
            (0, 16),
            f"Container: {containers}",
            font=font,
            fill=255
        )

        oled.image(image)
        oled.show()

        last_frame = frame

    time.sleep(10)