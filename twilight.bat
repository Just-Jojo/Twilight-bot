@ECHO OFF
:twily
CALL launcher.py
IF %ERRORLEVEL% NEQ 0 (
    CLS
    ECHO Restarting Twilight...
    GOTO twily
) ELSE (
    CLS
    GOTO RESTART
)
:RESTART
echo Would you like to restart?
set /P restart = "(y/n) "
if "%restart%" == "y" (
    goto twily
) else (
    echo Okay. Good day!
    cls
)