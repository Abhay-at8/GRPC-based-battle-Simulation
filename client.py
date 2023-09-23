import grpc
import random
import Soldier as s1

import game_pb2
import game_pb2_grpc
import time
from threading import Thread

t = 0


def run():
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
    print(obj)
    

    commander_thread = Thread(target=commander_activities, args=[obj, stub, T, commander_id])
    soldier_thread = Thread(target=soldier_action, args=[obj, stub, T, commander_id, N])

    commander_thread.start()
    soldier_thread.start()

    commander_thread.join()
    soldier_thread.join()


def commander_activities(obj, stub, T, commander_id):
    try:
        global t 
        print("Commnader is {}".format(commander_id))
        if obj.soldierID == commander_id and obj.alive:
            while t < T  and commander_id==obj.soldierID:
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
                print(res.message)
            
            time.sleep(10)

    except Exception as e:
        print(e)


def soldier_action(obj, stub, T, commander_id, N):
    response_iterator = stub.missile_approach(game_pb2.Empty())
    all_dead=False
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

            res = stub.is_commander_alive(
                    game_pb2.Empty())  # return the commanderId of current commander if alive else of
                # checking if old commander is dead and if the current soldier is the new commander
            if commander_id != res.commanderId and obj.soldierID == res.commanderId:
                commander_id = res.commanderId
                t=res.time
                var=res.all_dead
                print("I am new Commander")
                break
            #     print(f"Commander is dead with soldierId {commander_id}")
            #     print(f"Solider {obj.soldierID} is now the new commander.")
            #     # starting a new thread for the commander activities
            #     commander_thread = Thread(target=commander_activities, args=[obj, stub, T, res.commanderId])
            #     commander_thread.start()
            #     commander_thread.join()

        else:
            break
    print("out of Stream")
        




run()
