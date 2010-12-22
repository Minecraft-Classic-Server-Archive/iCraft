@ECHO off
TITLE iCraft
:input
set debug=
set /p debug=Do you want to turn on debugging? [Y/N] 
if "%debug%"=="" goto input
if "%debug%"=="y" goto debug
if "%debug%"=="n" goto nodebug
:debug
C:\Python26\python.exe run.py --debug
goto quit
:nodebug
C:\Python26\python.exe run.py
goto quit
:quit
PAUSE