@echo off
pushd %cd%\Idea
Anaconda
%UserProfile%\Anaconda\python.exe "%UserProfile%\Anaconda\Scripts/ipython-script.py" notebook
pause