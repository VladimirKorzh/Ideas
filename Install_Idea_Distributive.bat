@echo off

echo Welcome to the IDEA installation process.
:STEP1
GOTO ANACONDA
:STEP2
GOTO STOPWORDS
:STEP3
GOTO NOTEBOOKS
:STEP4
GOTO END

################################## INSTALLING ANACONDA PACKAGE
:ANACONDA
echo Determining the type of your system:
IF EXIST "%PROGRAMFILES(X86)%" (GOTO 64BIT) ELSE (GOTO 32BIT)

:64BIT
echo You have 64-bit Windows.
echo Running Anaconda Installation.
%cd%Anaconda\Anaconda-1.8.0-Windows-x86_64.exe
GOTO ANACONDAEND

:32BIT
echo You have 32-bit windows.
echo Running Anaconda Installation.
%cd%Anaconda\Anaconda-1.8.0-Windows-x86.exe
GOTO ANACONDAEND

:ANACONDAEND 
GOTO STEP2
################################# ~~~~~~~~~~~~~~~~~~~~~~~~~~~




################################# INSTALLING STOPWORDS
:STOPWORDS
echo Downloading stopwords Dictionary.
python -m nltk.downloader stopwords
GOTO STEP3
################################# ~~~~~~~~~~~~~~~~~~~~~~~~~~~




################################# INSTALLING NOTEBOOKS AND DATA
:NOTEBOOKS
%cd%Copy_Files_From_Flashdrive_to_Disk.bat
GOTO STEP4

################################ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~


:END
echo Installation Complete.
PAUSE 