# This script is used to run the server.py program with the specified arguments.
# The arguments are:

# arg1: The size of the battlefield matrix.
# arg2: The number of soldiers.
# arg3: The time/number of iterations.

# If the user forgets to include any of the arguments, the script will print an error message and exit.

# The script first creates a directory called `outputLogs` if it does not already exist. Then, it clears the contents
# of the `server.log` file. Finally, the script starts the server.py program with the specified arguments and
# redirects the output to the `server.log` file.

# To run the run_server.py script, open a terminal window and navigate to the directory where the script is located.
# Then, type the following command:

# python run_server.py arg1 arg2 arg3 arg4

# For example, to run the server.py program with a battlefield matrix size of 10, 3 soldiers, and 4 iterations,
# you would type the following command:

# python run_server.py 10 3 4 5

# The output of the server.py program will be redirected to the `server.log` file in the `outputLogs` directory.


import os
import sys

try:
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    arg3 = sys.argv[3]
    arg4 = sys.argv[4]

except:
    print("Fatal: You forgot to include the matrix size,no of soldiers, time/no of iteration.")
    print("Usage: python run_server.py arg1 arg2 arg3 -> Refer to readme.txt")
    sys.exit(1)

print("Got the args")

os.makedirs('outputLogs', exist_ok=True)

os.system('type nul > outputLogs/server.log')

print("starting server.py..")

os.system(f'python server.py {arg1} {arg2} {arg3} {arg4} > outputLogs/server.log')
