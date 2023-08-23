#!/bin/bash

# Actualizar repositorios
apt-get update

# Instalar dependencias de sistema
apt-get install -y ffmpeg

# Instalar paquetes de Python
packages=(
    pydub
    youtube_dl
    beautifulsoup4
    google-api-python-client
    moviepy
    telebot
    flask
    ffmpeg
    DBUtils
    yt-dlp
    validators
    pattern
    python-dotenv
    flask-cors
    Flask-Caching
    isodate
    matplotlib
    schedule
)

for package in "${packages[@]}"; do
    /home/ragde/python/virtual/bin/pip install "$package"
done
