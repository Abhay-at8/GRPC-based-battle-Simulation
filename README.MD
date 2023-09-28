<h1>Running the program</h1>

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Start the server:

```bash
python run_server.py arg1 arg2 arg3 arg4
```

* **arg1:** Battlefield dimensions (N)
* **arg2:** No of soldiers (M)
* **arg3:** Total time or no of iterations (T)
* **arg4:** max speed of soldiers (Smax)

3. Start the clients:

```bash
./run_client.bat arg2
```

* **arg2:** No. of separate soldier clients

4. Wait for the execution of the program to complete:

* Multiple command line windows will open each executing a separate soldier client.
* Descriptive messages are printed for each soldier
* Commander in addition also prints the battlefield layout after each iteration.
* After a game is finished, all terminal windows will close automatically otherwise close them manually.
* Press CTRL + C in the server terminal to close it.
* If it doesn't close, use the task manager to close the specific terminal process.
* Server output log will be saved in outputLogs/server.log file. Make sure server is closed otherwise server.log won't be saved.

5. Open the server.log file to see the descriptive output log messages that allows us to understand what happened in the war zone.

**Note:**

To run the server on a Linux VM system and the clients on Windows system:

1. In client.py at line 37, change the localhost to the IP address of the Linux VM system.
2. Based on your system, use either python or python3 to run the run_client.py script accordingly.
3. Also, in server.py, in the last line, change python to python3 based on your system.
4. If needed, server and clients can be run without the scripts. Run:

```bash
python server.py arg1 arg2 arg3 arg4
```
and then run 
```bash
python client.py arg2
```
arg2 times in separate terminals. This will produce the server log in the terminal itself instead of output.log file.


## Multiplayer Game in Python using gRPC-based Client-Server Architecture

**Program Design**

This multiplayer game is designed using a gRPC-based client-server architecture. Each client represents an individual soldier, and one of the soldiers is randomly chosen as the commander. The commander knows when the missile is approaching and sends this message to the server. The server then broadcasts this message to all the listening clients/soldiers using gRPC stream. All soldiers try to take shelter from the missile accordingly. The soldiers then send an update message to the game server with their new coordinates and status.

If the current commander dies, a new commander from the alive soldiers list is randomly selected. This process is repeated for T iterations. If at least 50% of the soldiers are alive after T iterations, the game is won. Otherwise, the game is lost.

**Hyperparameters**

The following hyperparameters are provided at runtime in the server terminal:

* **N:** Battlefield dimensions
* **M:** Number of soldiers
* **T:** Total time or number of iterations
* **Smax:** Maximum speed of the soldiers

**Commander**

The commander has the following functions:

* Sends a missile warning to the server after every t=1 unit-time.
* Prints the status of all soldiers.
* Send a wasHit() call to check status of a particular soldier
* Prints the battlefield layout.
* Prints the game status (won/lost) at the end of the game.

**Soldier**

A soldier has the following functions:

* Listens for missile approach warnings from the game server.
* When a missile approach warning is received, the soldier takes shelter from the missile.
* The soldier then sends an update message to the game server with its new coordinates and status.

**Server**

The server has the following functions:

* Provides methods for soldiers to register
* Updates their coordinates
* Receives missile coordinates.
* Maintains a list of all soldiers and missiles
* Updates the battlefield layout based on the soldiers' coordinates and the missile's trajectory
