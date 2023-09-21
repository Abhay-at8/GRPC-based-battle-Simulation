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
    
    
    cs=False
    # create a request with a message
    obj=s1.Soldier(x,y,s,int(response.message))
    print(obj)
    t=0
    #p = multiprocessing.Process(target=child)
    #p.start()
    
    if obj.soldierID==1 and cs==False:
      cs=True
      while t<7:
        print(f"sending missile {t} warning from commander\n\n")
        res=stub.sendMissile(game_pb2.Empty())
        t=t+1
        time.sleep(5)
      print("out of loop")
      if(t==6):
         res=stub.unary(game_pb2.Request(message="game over"))
    
    
    response_iterator = stub.missile_approach(game_pb2.Empty())
    cs==False

    #p.join()
    if(True):
    # iterate over the responses and print them
      for res in response_iterator:
        #res = stub.missile_approach(game_pb2.Empty())
        m=s1.Missile(res.x,res.y,res.rad)
        obj.take_shelter(m,10)
      #time.sleep(5)
    
    # while obj.alive:
    #   res = stub.missile_approach(game_pb2.Empty())
    #   m=s1.Missile(res.x,res.y,res.rad)
    #   obj.take_shelter(m,10)
    #   time.sleep(5)

   
   
run()