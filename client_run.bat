


FOR /L %%y IN (1, 1, 3) DO (

start python client.py >>%%y%%.txt
timeout /t 3
)
PAUSE


