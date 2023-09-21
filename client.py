import grpc
import random
import Soldier as s1

import game_pb2
import game_pb2_grpc
import time,os
import multiprocessing
from threading import Thread
#
def child():
    print("In the child process that has the PID {}".format(os.getpid())) 

def run():
#    with grpc.insecure_channel('localhost:50051') as channel:
#       stub = game_pb2_grpc.GreeterStub(channel)
#       #response = stub.greet(game_pb2.ClientInput(name='John', game = "Yo"))
#       x=random.randint(0,10)
#       y=random.randint(0,10)
#       s=random.randint(1,4)
#       response = stub.register(game_pb2.Soldier(x=x, y=y,speed=s))
    

#    print("Greeter client received following from server: " + response.message)
#    obj=Soldier.Soldier(x,y,s,int(response.message))
#    print(obj)
    channel = grpc.insecure_channel("localhost:50051")
  # create a stub for the service
    stub = game_pb2_grpc.GameStub(channel)

    x=random.randint(0,10)
    y=random.randint(0,10)
    s=random.randint(1,4)
    response = stub.register(game_pb2.Soldier(x=x, y=y,speed=s))
    
    is_commander=False
    cs=False
    # create a request with a message
    obj=s1.Soldier(x,y,s,int(response.message))
    print(obj)
    t=0
    #p = multiprocessing.Process(target=child)
    #p.start()
    try:

      if obj.soldierID==1 and cs==False:
        cs=True
        is_commander=True
        while t<4:
          print(f"sending missile {t} warning from commander\n\n")
          res=stub.sendMissile(game_pb2.Empty())
          t=t+1
          time.sleep(5)
          res=stub.status_all(game_pb2.Empty())
          print(res.message)
        print("out of loop")
        if(t==5):
          res=stub.unary(game_pb2.Request(message="game over"))
        time.sleep(10)
        #res=stub.unary(game_pb2.Request(message="print"))
    except Exception as e:
      print(e)
    
    
    response_iterator = stub.missile_approach(game_pb2.Empty())
    #cs==False

    #p.join()
    if(not is_commander):
    # iterate over the responses and print them
      for res in response_iterator:
        #res = stub.missile_approach(game_pb2.Empty())
        if(obj.alive):
          m=s1.Missile(res.x,res.y,res.rad)
          msg=obj.take_shelter(m,10)
          print(msg)
          req=stub.update_cordinates(game_pb2.Update(alive=obj.alive,x=obj.x_cord,y=obj.y_cord,message=msg))
        else:
          break


   

run()

