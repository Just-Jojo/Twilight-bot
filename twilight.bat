@ECHO OFF
:twily
CALL launcher.py
IF %ERRORLEVEL% NEQ 0 (
    CLS
    ECHO Restarting Twilight...
    GOTO twily
) ELSE (
    CLS
)