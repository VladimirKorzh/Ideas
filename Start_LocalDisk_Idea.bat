@echo on

Pushd "%UserProfile%\Documents\IPython Notebooks"
Anaconda
%UserProfile%\Anaconda\python.exe "%UserProfile%\Anaconda\Scripts/ipython-script.py" notebook
pause