FOR /L %%y IN (0, 1, 2) DO (
start python client.py
timeout /t 3
)
PAUSE


