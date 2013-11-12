@echo off
pushd %cd%\Idea
%UserProfile%\Anaconda\python.exe "%UserProfile%\Anaconda\Scripts/ipython-script.py" notebook
pause