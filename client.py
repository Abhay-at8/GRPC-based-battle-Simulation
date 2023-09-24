import grpc
import random
import Soldier as s1

import game_pb2
import game_pb2_grpc
import time
from threading import Thread

# Global variable to track the current time step.



def run():
    global t
    global commander_id
    t=0

    """Starts a new game session for the soldier.

    This function performs the following steps:

    1. Initializes a new game session with the game server.
    2. Registers the soldier with the game server.
    3. Starts two threads:
        * A commander thread that will manage the soldier's movements and attacks.
        * A soldier thread that will execute the commander's instructions.
    4. Waits for both threads to finish before returning.
    """

    N = 10
    M = 3
    T = 5

    channel = grpc.insecure_channel("localhost:50051")
    # create a stub for the service
    stub = game_pb2_grpc.GameStub(channel)
    res = stub.initiaze(game_pb2.Empty())

    commander_id = res.sol_id
    N = res.N  # Battlefield Matrix size
    M = res.M  # No of soldiers along with commander
    T = res.T  # Time or no of missiles firings

    x = random.randint(0, N - 1)
    y = random.randint(0, N - 1)
    s = random.randint(1, 4)
    response = stub.register(game_pb2.Soldier(x=x, y=y, speed=s))

    # create a request with a message
    obj = s1.Soldier(x, y, s, int(response.message))

    border_msg(obj.__str__())

    commander_thread = Thread(target=commander_activities, args=[obj, stub, T ])
    soldier_thread = Thread(target=soldier_action, args=[obj, stub, T, N])

    commander_thread.start()
    soldier_thread.start()

    commander_thread.join()
    soldier_thread.join()


def commander_activities(obj, stub, T, ):
    """The commander thread function.

    This function performs the following steps:

    1. Sends a missile warning to all soldiers every t seconds.
    2. Prints the status of all soldiers.
    3. Prints the battlefield layout.
    4. Waits for the game to end.
    5. Prints the game status at the end of the game.

    Args:
        obj: The soldier object.
        stub: The game stub object.
        T: The time or number of missile firings.
    """

    try:
        global t 
        global commander_id
        while t<T and obj.alive:
            
            if obj.soldierID == commander_id and obj.alive:
                print("Commnader is {}".format(commander_id))
                while t < T  and obj.alive:
                    print(f"sending missile {t} warning from commander\n\n")
                    res = stub.sendMissile(game_pb2.Empty())
                    t = t + 1
                    time.sleep(10)
                    res = stub.status_all(game_pb2.Empty())
                    print(res.message)
                    time.sleep(5)
                    res = stub.print_layout(game_pb2.Empty())
                    print(res.message)
                    print('\n')
                    
                    print("--------------------------------------")
                print("Game ends here")
            
            if t==T:
                res = stub.game_status(game_pb2.Empty())
                border_msg(res.message)
            
            time.sleep(10)
        exit()

    except Exception as e:
        print(e)


def soldier_action(obj, stub, T, N):
    """The soldier thread function.

    This function performs the following steps:

    1. Listens for missile approach warnings from the game server.
    2. When a missile approach warning is received, the soldier takes shelter from the missile.
    3. The soldier then sends an update message to the game server with its new coordinates and status.

    Args:
        obj: The soldier object.
        stub: The game stub object.
        T: The time or number of missile firings.
        N: The battlefield matrix size.
    """
    global t
    global commander_id

    response_iterator = stub.missile_approach(game_pb2.Empty())
    # all_dead = False
    # iterate over the responses and print them
    for res in response_iterator:
        # res = stub.missile_approach(game_pb2.Empty())
        if obj.alive:
            m = s1.Missile(res.x, res.y, res.rad)
            msg = obj.take_shelter(m, N)
            print(msg)
            req = stub.update_cordinates(
                game_pb2.Update(alive=obj.alive, x=obj.x_cord, y=obj.y_cord, message=msg,
                                soldierID=obj.soldierID))

            res = stub.is_commander_alive(game_pb2.Empty())  
            if res.all_dead:
                t=T
                print("All dead")
                break

            if commander_id != res.commanderId and obj.soldierID == res.commanderId:
                time.sleep(5)
                commander_id = res.commanderId
                print(f"commander dead : before t")
                t=res.time
                var=res.all_dead
                print(f"After t {t}")
                print("I am new Commander")
                time.sleep(2)
            if not obj.alive:
                break
                

        else:
            break
    print("out of Stream")
    if obj.alive:
        t=T


def border_msg(msg):
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


run()
