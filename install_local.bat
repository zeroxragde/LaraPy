@echo off
pip install --upgrade pip
REM Instalar paquetes de Python
set "packages=pydub youtube_dl beautifulsoup4 google-api-python-client moviepy telebot flask ffmpeg yt-dlp validators pattern DBUtils python-dotenv flask-cors Flask-Caching isodate matplotlib schedule"

for %%p in (%packages%) do (
    pip install %%p
)
pause