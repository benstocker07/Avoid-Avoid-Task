@echo off

echo Running from: %~dp0

echo Welcome to the task! This won't take long.
echo.
echo Setting you up now...
echo.

py Install.py

echo.
echo Completed installation
echo.


py "OED Task.py"

pause
