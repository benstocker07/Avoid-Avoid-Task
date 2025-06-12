@echo off

echo Running from: %~dp0

echo Welcome to the task! This won't take long.
echo.
echo Setting you up now...
echo.

pip install pygame pandas joystick numpy scipy matplotlib timer pymysql requests

REM py Install.py

echo.
echo Completed installation
echo.


py "OED Task.py"

pause
