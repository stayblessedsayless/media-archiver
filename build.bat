@echo off
cd /d %~dp0
py -m pip install pyinstaller
pyinstaller --onefile --windowed media_archiver.py
pause
