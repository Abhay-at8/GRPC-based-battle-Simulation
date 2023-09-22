import grpc
import random
import Soldier as s1

import game_pb2
import game_pb2_grpc
import time, os
import multiprocessing
from threading import Thread


def child():
    print("In the child process that has the PID {}".format(os.getpid()))


def run():
    N = 10
    M = 3
    T = 5

    channel = grpc.insecure_channel("localhost:50051")
    # create a stub for the service
    stub = game_pb2_grpc.GameStub(channel)
    res = stub.initiaze(game_pb2.Empty())
    N = res.N
    M = res.M
    T = res.T

    x = random.randint(0, 10)
    y = random.randint(0, 10)
    s = random.randint(1, 4)
    response = stub.register(game_pb2.Soldier(x=x, y=y, speed=s))

    is_commander = False
    cs = False
    # create a request with a message
    obj = s1.Soldier(x, y, s, int(response.message))
    print(obj)
    # t = 0
    # commander_activities(obj, stub, is_commander, cs, T)
    # soldier_action(obj, stub, is_commander, N)

    commander_thread = Thread(target=commander_activities, args=[obj, stub, is_commander, cs, T])
    soldier_thread = Thread(target=soldier_action, args=[obj, stub, is_commander, N])

    commander_thread.start()
    soldier_thread.start()

    commander_thread.join()
    soldier_thread.join()


def commander_activities(obj, stub, is_commander, cs, T):
    try:
        t = 0
        if obj.soldierID == 1 and cs == False:
            cs = True
            is_commander = True
            while t < T:
                print(f"sending missile {t} warning from commander\n\n")
                res = stub.sendMissile(game_pb2.Empty())
                t = t + 1
                time.sleep(5)
                res = stub.status_all(game_pb2.Empty())
                print(res.message)
                time.sleep(5)
                res = stub.print_layout(game_pb2.Empty())
                print(res.message)
                print('\n')
            print("Game ends here")
            res = stub.game_status(game_pb2.Empty())
            print(res.message)

            time.sleep(10)

    except Exception as e:
        print(e)


def soldier_action(obj, stub, is_commander, N):
    response_iterator = stub.missile_approach(game_pb2.Empty())
    # cs==False

    # p.join()
    if not is_commander:
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
            else:
                break


run()
