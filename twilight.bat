@ECHO OFF
:twily
CALL launcher.py
IF "%SHUTDOWNLEVEL%" == 26 (
    CLS
    ECHO Restarting Twilight...
    GOTO twily
) ELSE (
    CLS
)