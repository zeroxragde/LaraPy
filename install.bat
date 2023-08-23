@echo off

REM Instalar paquetes de Python
set "packages=pydub youtube_dl beautifulsoup4 google-api-python-client moviepy telebot flask ffmpeg yt-dlp validators pattern DBUtils python-dotenv flask-cors Flask-Caching isodate matplotlib schedule"

for %%p in (%packages%) do (
    "venv\Scripts\pip" install %%p
)
pause