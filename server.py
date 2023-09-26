from concurrent import futures

import grpc
import game_pb2
import game_pb2_grpc
import Soldier as s1
import time, random
import sys

game_end = False


class Game(game_pb2_grpc.GameServicer):
    """
    A gRPC server that provides methods for soldiers to register, update their coordinates, and receive missile
    coordinates.

    The server also maintains a list of all soldiers and missiles, and updates the battlefield layout based on the
    soldiers' coordinates and the missile's trajectory.
    """
    soldierId = 0
    soldiers = []
    commander_alive = True
    update_cntr = 0
    soldier_msg_list = ""
    alive_soldiers = [i for i in range(1, int(sys.argv[2]) + 1)]

    def __init__(self):
        """
           Initializes a new game.

           This function initializes the list of soldiers, the list of missiles, the current missile iteration, and the commander ID.
        """

        self.clients = []  # a list to store the connected soldier clients
        self.missiles = []  # a list to store the missile objects
        self.dead_soldiers = []  # a list to store dead soldier objects
        self.game_over = False  # game over flag
        self.t = 0  # running time
        dead_in_iteration=""

        # storing hyperparameters from command line args into Game object attributes N, M and T.
        try:
            self.N = int(sys.argv[1])  # Battlefield Matrix size
            self.M = int(sys.argv[2])  # No of soldiers along with commander
            self.T = int(sys.argv[3])  # Time or no of missiles firings
            self.S = int(sys.argv[4])  # max speed of soldier
            
            # setting one of the M soldiers as initial commander randomly
            self.commanderId = random.randint(1, self.M)
            # print(f"GAME STARTING....\nSoldier {self.commanderId} is commander\n")
            print(f"GAME STARTING....\n")
            

        except:
            print("Fatal: You forgot to include the matrix size,no of soldiers, time/no of iteration, Soldiers max speed.")
            print("Usage: python server.py arg1 arg2 arg3 arg4-> Refer to readme.txt")
            sys.exit(1)

    def border_msg(self, msg):
        """ Prints a message with a border around it.

         Args:
             msg: The message to print.
         """

        # Split the message into lines.
        msg_lines = msg.split('\n')

        # Find the longest line in the message.
        max_length = max([len(line) for line in msg_lines])

        # Calculate the number of characters in the border.
        count = max_length + 2

        # Create the border string.
        dash = "*" * count

        # Print the top border.
        print("*%s*" % dash)

        # Iterate over the message lines and print them with the border.
        for line in msg_lines:
            # Calculate the number of spaces to pad the line to the border.
            half_dif = (max_length - len(line))

            # If the line is the same length as the border, print it without padding.
            if half_dif == 0:
                print("* %s *" % line)
            # Otherwise, print the line with padding to the border.
            else:
                print("* %s " % line + ' ' * half_dif + '*')

        # Print the bottom border.
        print("*%s*" % dash)

    def game_status(self, request, context):
        """
         Checks the status of the game and returns a message indicating whether the game is won or lost.

         This function checks the number of soldiers that are still alive and compares it to half the total number of 
         soldiers. If the number of alive soldiers is greater than or equal to half the total number of soldiers, 
         the game is won. Otherwise, the game is lost. 

         Args:
             request: A game_pb2.Empty object.
             context: A grpc.server.Context object.

         Returns:
             A game_pb2.Response object containing a message indicating whether the game is won or lost.
         """
        time.sleep(5)
        if self.M-len(self.dead_soldiers) < 0.5 * self.M:
            msg = f"{len(self.soldiers)} out of {self.M} are alive. Game is won !!!!"
        else:
            msg = f"{len(self.soldiers)} out of {self.M} are alive. Game is lost :("

        game_end = True

        # print(msg)
        self.border_msg(msg)

        return game_pb2.Response(message=msg)

    def initiaze(self, request, context):
        """
        Sends the initial values of the game to the client, including the commander ID, battlefield matrix size,
        number of soldiers, and number of missile firings and max speed of soldier.

        Args:
            request: A game_pb2.Empty object.
            context: A grpc.server.Context object.

        Returns:
            A game_pb2.InitialValues object with the initial values of the game.
        """

        return game_pb2.InitialValues(commander_id=self.commanderId, N=self.N, M=self.M, T=self.T, S=self.S)

    def status_all(self, request, context):
        """
        Prints the status of all soldiers to the console and returns a message to the client with the status of all
        soldiers.

            The function first prints a message to the console indicating that the commander has requested the status
            of all soldiers. It then waits for all soldiers to send their status updates. Once all updates have been
            received, the function prints the status of all soldiers to the console and returns a message to the
            client with the status of all soldiers.

            Args:
                request: A game_pb2.Request object.
                context: A grpc.server.Context object.

            Returns:
                A game_pb2.Response object with the status of all soldiers.
        """
        self.dead_in_iteration=""
        print(f"\nCommander requested status of all soldier.\nWaiting for updates...\n\n")
        while True:
            if self.update_cntr == len(self.soldiers):
                print(f"{self.soldier_msg_list}")
                self.soldier_msg_list = ""
                self.update_cntr = 0
                time.sleep(5)
                break

        msg = "\n"
        #print(f"iterating soldiers in statusall {len(self.soldiers)}\n\n")

        time.sleep(1)
        for soldier in self.soldiers:
            # print(f"before: {soldier}\n")
            msg += f"soldier Id : {soldier.soldierID}"

            if soldier.alive:
                msg += ", status : alive\n"
                #print(f"Alive {soldier.soldierID} from alive soldiers")
            else:
                msg += ", status : dead\n"
                self.dead_soldiers.append(soldier.soldierID)
                self.dead_in_iteration+=f"{soldier.soldierID} "
                #self.soldiers.remove(soldier)


        for soldier in self.soldiers:
            if not soldier.alive:
                self.soldiers.remove(soldier)  

        #print(f"In staus_all: Status of soldiers is as follows\n{msg}\n")
        time.sleep(5)
        print(msg)
        return game_pb2.Response(message=msg)

    def update_cordinates(self, request, context):
        """
        Updates the coordinates of the soldier with the given ID.

        This function is called by soldier clients to send their updated coordinates to the commander. The commander
        then updates the coordinates of the soldier in its list of soldiers. If the soldier is dead, the function
        removes the soldier from the list of alive soldiers. If the dead soldier is the commander, the function sets
        the `commander_alive` flag to `False`.

        Args:
            request: A game_pb2.UpdateCordinatesRequest object containing the soldier's updated coordinates.
            context: A grpc.server.Context object.

        Returns:
            A game_pb2.Empty object.
        """

        # print(f"\n updates recieved {request}\n")
        
        # print(f"Update_cntr: {self.update_cntr}\n")N

        self.soldier_msg_list += f"{request.message} \n"
        for soldier in self.soldiers:
            # print(f"before: {soldier}\n")
            if soldier.soldierID == request.soldierID:
                if request.alive:
                    soldier.x_cord = request.x
                    soldier.y_cord = request.y
                else:
                    soldier.alive = False
                    self.alive_soldiers.remove(int(soldier.soldierID))
                    #print(f"In Update_cords:Removed {soldier.soldierID} from alive soldiers")
                    if soldier.soldierID == self.commanderId:
                        print("Commander died")
                        # if int(soldier.soldierID) in self.alive_soldiers:
                        # print("Deleting commander from alive list")

                        self.commander_alive = False
            # print(f"after: {soldier}\n\n")
        self.update_cntr += 1

        return game_pb2.Empty()

    # registering each soldier client that connects to the server
    def register(self, request, context):
        """
         Registers a new soldier with the game.

         This function is called by soldier clients to register themselves with the game. The function assigns a
         unique ID to the soldier and adds it to the list of soldiers.

         Args:
             request: A game_pb2.RegisterRequest object containing the soldier's initial coordinates and speed.
             context: A grpc.server.Context object.

         Returns:
             A game_pb2.ServerOutput object containing the soldier's unique ID and -1 if no client > N.
         """
        if(self.soldierId==self.M ):
            print(f"{self.M} Clients already connected. Cannot connect anymore clients")
            return game_pb2.ServerOutput(message="-1")
        self.soldierId += 1
        sol_id = self.soldierId
        sol = s1.Soldier(request.x, request.y, request.speed, self.soldierId)
        self.soldiers.append(sol)
        print(f"Registered soldier {sol_id} (x:{request.x},y:{request.y})\n")
        # print(sol_id)
        # print(f"Got request {request}\n" )
        time.sleep(2)
        # while True:
        #     if(len(self.soldiers)==3):
        #         break
        if len(self.soldiers) == self.M:
            print(f"Soldier {self.commanderId} chosen as the commander\n")

        return game_pb2.ServerOutput(message="{0}".format(self.soldierId))

    def sendMissile(self, request, context):
        def sendMissile(self, request, context):
            """
            Sends a missile to a random location on the battlefield.

            This function is called by the commander to send a missile to a random location on the battlefield. The
            function creates a new missile object and adds it to the list of missiles. The function also increments
            the missile iteration counter.

            Args:
                request: A game_pb2.Empty object.
                context: A grpc.server.Context object.

            Returns:
                A game_pb2.Empty object.
            """

        # print(f"No of participants:{self.M}")
        while True:
            if len(self.soldiers) + len(self.dead_soldiers) == self.M:
                break

        time.sleep(5)
        x = random.randint(0, self.N - 1)
        y = random.randint(0, self.N - 1)
        s = random.randint(1, 4)
        m = s1.Missile(x_cord=x, y_cord=y, rad=s)
        self.missiles.append(m)
        self.t += 1
        outputStr = f"Missile Iteration {self.t}:\nWarning from commander: Missile {self.t} approaching {m}"
        self.border_msg(outputStr)
        print("\n")

        if self.t == self.T:
            time.sleep(5)
            self.game_over = True
        return game_pb2.Empty()
    
    def was_hit(self, request, context):
        """
        checks if a soldier was hit or not and returns True value if hit

        Args:
                request: A game_pb2.Empty object.
                context: A grpc.server.Context object.

        Returns:
                A game_pb2.wasHit object which return flag and soldier id if hit.

        """
        print(f"Got was hit call from commander for soldier {request.soldierID}\n")
        x=request.soldierID
        if x in self.dead_soldiers:
            print(f"Soldier {x} was hit")
            request.trueFlag=True
        else:
            print(f"Soldier {x} was not hit")
        return game_pb2.wasHit(soldierID=x,trueFlag=request.trueFlag)


    def missile_approach(self, request, context):
        """
            Streams the coordinates of approaching missiles to the client.

            This function is called by the client to receive the coordinates of approaching missiles. The function
            streams the coordinates of all approaching missiles to the client.

            Args:
                request: A game_pb2.Empty object.
                context: A grpc.server.Context object.

            Yields:
                A game_pb2.Missile object containing the coordinates of an approaching missile.
        """
        # print(f"attacking with missile\n")
        attack = 0
        while not self.game_over:
            while len(self.missiles) > attack:
                m = self.missiles[attack]
                # print(f"attacking with missile {attack} : {m}")
                attack += 1
                yield game_pb2.Missile(x=m.x_cord, y=m.y_cord, rad=m.rad)
        # print(f"missile attack over")

    def print_layout(self, request, context):
        """
        Prints the layout of the battlefield to the console.

        This function prints the layout of the battlefield to the console, including the locations of all soldiers
        and the missile. The function also marks the missile's trajectory with '#' characters.

        Args:
            request: A game_pb2.Request object.
            context: A grpc.server.Context object.

        Returns:
            A game_pb2.Request object containing a message with the layout of the battlefield.
        """
        N = self.N
        missile = self.missiles[self.t - 1]
        print(f"The layout of battle field:\n")

        # list for printing soldiers
        # soldierSet = []

        # for soldier in self.soldiers:
        #     # appending a tuple of the soldier coordinates to the list
        #     soldierSet.append((soldier.x_cord, soldier.y_cord))

        # print(f"Alive soldiers coordinates on the battlefield: {soldierSet}")

        obj_map = [(soldier.soldierID, soldier.x_cord, soldier.y_cord) for soldier in self.soldiers if soldier.alive]


        print(f"Alive soldiers on the battlefield in current iteration {self.t}:")
        if(len(obj_map)==0):
            print("None")
        for soldierID, x, y in obj_map:
            print(f"{soldierID}({x},{y})", end=" ")
        print(f"\nDead soldiers in current iteration {self.t}:")
        if(len(self.dead_soldiers)==0):
            print("None")
        else:
            print(self.dead_in_iteration)

        mat = [['.' for x in range(N)] for y in range(N)]

        for soldierID, x, y in obj_map:
            # assigning the soldier ID to the matrix cell
            mat[y][x] = soldierID

        for i in range(N):
            for j in range(N):
                if i == missile.top_bdry or i == missile.bottom_bdry:
                    if missile.left_bdry <= j <= missile.right_bdry and mat[i][j] == '.':
                        mat[i][j] = '#'
                if j == missile.right_bdry or j == missile.left_bdry:
                    if (missile.bottom_bdry >= i >= missile.top_bdry) and mat[i][j] == '.':
                        mat[i][j] = '#'

        # mark missile coordinate on the matrix
        print(f"\nMissile {missile}\n")
        mat[missile.y_cord][missile.x_cord] = 'X'

        # print(mat)
        # print the matrix row by row
        msg = "\n"
        for row in mat:
            print(*row)
            for i in row:
                msg += f"{str(i)} "
            msg += "\n"
        print(f"\nIteration {self.t} over\n\n")


        return game_pb2.Request(message=msg)

    def is_commander_alive(self, request, context):
        """
        Checks if the commander is alive and returns the commander's ID and the current missile iteration.

        This function is called by the client to check if the commander is alive and to get the commander's ID and
        the current missile iteration. The function returns a `game_pb2.Commander_alive_response` object containing
        the commander's ID, the current missile iteration, and a flag indicating whether all soldiers are dead.

        Args:
            request: A game_pb2.Empty object.
            context: A grpc.server.Context object.

        Returns: A game_pb2.Commander_alive_response object containing the commander's ID, the current missile
        iteration, and a flag indicating whether all soldiers are dead.
        """

        while True:
            if self.update_cntr==len(self.soldiers):
                time.sleep(2)
                break

        all_dead=False
        if not self.commander_alive:
            if len(self.alive_soldiers)>0:
                index = random.randint(0, len(self.alive_soldiers)-1)
                self.commanderId=self.alive_soldiers[index]
            else:
                all_dead=True
            # while not self.soldiers[index].alive:
            #     index = random.randint(0, len(self.soldiers) - 1)
            #self.commanderId=self.soldiers[index].soldierID
            self.commander_alive=True
            if all_dead:
                print(f"commander along with other soldiers died..cannot choose new commander")
            else:
                print(f"Commander died. New commnder is soldier{self.commanderId}\n")
        return game_pb2.Commander_alive_response(commanderId=self.commanderId,time=self.t,all_dead=all_dead)


def server():
    """
    Starts a gRPC server that listens on port 50051.

    The server exposes the `Game` service, which provides methods for soldiers to register, update their coordinates, and receive missile coordinates.

    This function blocks until the server is terminated.
    """

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=11))
    game_pb2_grpc.add_GameServicer_to_server(Game(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    # if(game_end):
    #     exit(1)
    server.wait_for_termination()


server()
