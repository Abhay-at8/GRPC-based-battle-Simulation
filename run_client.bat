@echo off

REM This batch file is used to run the client.py program multiple times.
REM The number of times the program is run is specified by the first argument to the batch file.

REM For example, to run the client.py program 10 times, you would execute the following command:

REM run_client.bat 10

REM The batch file works by using a FOR loop to iterate from 1 to the specified number of clients.
REM For each iteration, the batch file starts a new instance of the client.py program.
REM The batch file also uses the timeout command to wait for 3 seconds before starting the next client.
REM This is to prevent the server from being overwhelmed by too many concurrent client connections.

REM After all of the client programs have been started, the batch file pauses.
REM This allows you to view the output of the client programs in the console window.

REM To exit the batch file, press any key.


FOR /L %%y IN (1, 1, %1) DO (

start python client.py
timeout /t 3
)
PAUSE


