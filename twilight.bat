@ECHO OFF
:RESTART
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
ECHO  Would you like to restart?
SET /P restart = "(y/n) "
IF "%restart%" == "y" (
    GOTO twily
) ELSE (
    ECHO Okay. Good day!
    CLS
)