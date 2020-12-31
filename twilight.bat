@ECHO OFF
:TWILY
CALL launcher.py
IF %ERRORLEVEL% NEQ 0 (
    CLS
    ECHO Restarting Twilight...
    GOTO TWILY
) ELSE IF %ERRORLEVEL% == 1 (
    ECHO There is an issue. Please read the traceback!
    SET /P read = "> "
    IF "%read%" == "y" (
        GOTO TWILY
    ) ELSE (
        ECHO Okay!
    )
)  ELSE (
    CLS
    GOTO RESTART
)
:RESTART
ECHO  Would you like to restart?
SET /P restart = "(y/n) "
IF "%restart%" == "y" (
    GOTO TWILY
) ELSE (
    ECHO Okay. Good day!
    CLS
)
