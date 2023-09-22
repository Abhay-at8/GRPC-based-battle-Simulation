FOR /L %%y IN (0, 1, 8) DO (
start python client.py
timeout /t 3
)
PAUSE


