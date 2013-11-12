@echo off
echo Removing IDEA Distributive.
rmdir /s /q "%UserProfile%\My Documents\IPython Notebooks"
%USERPROFILE%\Anaconda\Uninstall-Anaconda.exe
echo Removal complete
pause
