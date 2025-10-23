@echo off
cd \Users\Public\Ben\rJORT
echo Running from: %~dp0

python LoadingWindow.py
python STAI.py
python EPQ.py
python rJORT.py
