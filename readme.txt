**************
Group Details:
**************
1. Abhay Tripathi -> 2023H1120190P
2. Shubham Kumar  -> 2023H1120191P


********************
Running the program
********************

Please also check the note below.
1. pip install -r requirement.txt
2. Start the server
	• python run_server.py arg1 arg2 arg3 arg4
	• it starts the server.py and logs its output in outputLogs/server.log file.
	• Arguments are the hyperparameters:
		o arg1: Battlefield dimensions (N)
		o arg2: No of soldiers (M)
		o arg3: Total time or no of iterations (T)
		o arg4: max speed of soldiers (Smax)

3. Start the clients
	• ./run_client.bat arg2
	• Run run_client.bat which starts n separate clients
	• arg2 is the no. of separate soldier clients 

4. Wait for the execution of the program to complete
	• Multiple command line windows will open each executing a separate soldier client.
	• Descriptive messages are printed for each soldier
	• Commander in addition also prints the battlefield layout after each iteration.
	• After a game is finished [see the output message in the commander window], all terminal windows will close automatically otherwise close them manually.
	• Press CTRL + C in the server terminal to close it.
	• If it doesn’t close, use the task manager to close the specific terminal process.
	• Server output log will be saved in outputLogs/server.log file. Make sure server is closed otherwise server.log won’t be saved.

5. Open the server.log file to see the descriptive output log messages that allows us to understand what happened in the war zone.

*****
Note:
*****
To run the server on a Linux VM system and the clients on Windows system:
1. In client.py at line 37, change the localhost to the IP address of the Linux VM system.
	• Example:
	# Change this:
	channel = grpc.insecure_channel("localhost:50051")
	# To this:
	channel = grpc.insecure_channel("192.168.181.3:50051")

2. Based on your system, use either python or python3 to run the run_client.py script accordingly.
	• Example:
	# On a system with Python 3 installed:
	python3 run_server.py arg1 arg2 arg3 arg4
	# On a system with Python 2 installed:
	python run_server.py arg1 arg2 arg3 arg4

3. Also, in server.py, in the last line, change python to python3 based on your system.
	• Example:
	# Change this:
	os.system(f'python server.py {arg1} {arg2} {arg3} {arg4} > outputLogs/server.log')
	# To this:
	os.system(f'python3 server.py {arg1} {arg2} {arg3} {arg4} > outputLogs/server.log')

4. If needed, server and clients can be run without the scripts.
	Run: 
	"python server.py arg1 arg2 arg3 arg4" and then run "python client.py arg2" ,  arg2 times in separate terminals
	This will produce the server log in the terminal itself instead of output.log file.
