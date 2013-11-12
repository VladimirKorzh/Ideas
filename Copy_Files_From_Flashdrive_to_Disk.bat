@echo off

echo Starting restore process.
echo it will copy all your IDEA files from the flashdrive to your local drive

:NOTEBOOKS
echo Determining Windows version
IF EXIST "%USERPROFILE%\My Documents" (GOTO WINXP) ELSE (GOTO WIN7)

:WINXP
echo You are running Windows XP
echo Copying Notebook Files.
mkdir "%UserProfile%\My Documents\IPython Notebooks"
xcopy %cd%Idea "%UserProfile%\My Documents\IPython Notebooks" /y /s
GOTO END

:WIN7
echo You are running Windows Vista or higher
echo Copying Notebook Files.
mkdir "%UserProfile%\Documents\IPython Notebooks"
xcopy %cd%Idea "%UserProfile%\Documents\IPython Notebooks" /y /s
GOTO END

:END
echo Restore complete
PAUSE