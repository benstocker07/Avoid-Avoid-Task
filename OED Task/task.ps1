Write-Host "Welcome to the task! This won't take long.`n"
Write-Host "Setting you up now...`n"
pip install pygame paramiko pandas matplotlib pymysql statsmodels numpy scipy joystick timer setuptools

Write-Host "`nRunning Install.py..."
py Install.py

Write-Host "`nCompleted installation`n"

Write-Host "Running OED Task.py..."
py "OED Task.py"

Read-Host -Prompt "Press Enter to continue..."
pause