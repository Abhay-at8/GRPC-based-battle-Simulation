import platform
import os
import sys

arg1 = sys.argv[1]

if platform.system() == "Windows":
    os.system(f'run_client.bat{arg1}')
else:
    # Code that is compatible with both Windows and Linux
    pass