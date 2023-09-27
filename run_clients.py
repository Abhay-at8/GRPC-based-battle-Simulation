import subprocess
import sys
from time import sleep


python_bin = "venv\\Scripts\\python"

# Path to the script that must run under the virtualenv
script_file = "client.py"
for i in range(0,int(sys.argv[1])):
    subprocess.Popen([python_bin, script_file])
    sleep(5)
