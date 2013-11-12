@echo off


echo Starting backup process.
echo it will copy all your local IDEA files onto the flashdrive

:NOTEBOOKS
echo Determining Windows version
IF EXIST "%USERPROFILE%\My Documents" (GOTO WINXP) ELSE (GOTO WIN7)

:WINXP
echo You are running Windows XP
echo Copying Notebook Files.
xcopy "%UserProfile%\My Documents\IPython Notebooks" %cd%Idea /y
GOTO STEP4

:WIN7
echo You are running Windows Vista or higher
echo Copying Notebook Files.
xcopy "%UserProfile%\Documents\IPython Notebooks" %cd%Idea /y
GOTO STEP4

:STEP4
echo Backup Complete
PAUSE