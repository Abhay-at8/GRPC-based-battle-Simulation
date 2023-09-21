from concurrent import futures

import grpc
import game_pb2
import game_pb2_grpc
import Soldier as s1
import time,random

class Game(game_pb2_grpc.GameServicer):
    def __init__(self):
    # a list to store the connected clients
        self.clients = []
        self.missiles=[]
        self.game_over=False


    def broadcast(self,request,context):
        t=0
        print(f"Received message from client: {request.message}")
        while True:
            response = game_pb2.Response(message=f"missile approaching : {t}")
            
            #response.message()
            yield response
            time.sleep(2)

            response.message=f"status {t}"
            yield response
            time.sleep(2)

            t+=1
            if t==4:
                break





    soldierId=0
    soldiers=[]

#    def greet(self, request, context):
#       print("Got request " + str(request))
#       return game_pb2.ServerOutput(message='{0} {1}!'.format(request.game, request.name))
    def register(self, request, context):
        self.soldierId+=1;
        #sol_id=self.soldierId
        sol=s1.Soldier(request.x,request.y,request.speed,self.soldierId)
        self.soldiers.append(sol)
        #rint(f"Registered a soldier {sol_id}\n")
        #print(sol_id)
        print(f"Got request {request}\n" )
        time.sleep(5)
        # while True:
        #     if(len(self.soldiers)==3):
        #         break
        return game_pb2.ServerOutput(message='{0}'.format(self.soldierId))
    
    def sendMissile(self, request, context):
        while True:
            if(len(self.soldiers)==3):
                break
        x=random.randint(0,10)
        y=random.randint(0,10)
        s=random.randint(1,4)
        m=s1.Missile(x_cord=x,y_cord=y,rad=s)
        self.missiles.append(m)
        return game_pb2.Empty()
    
    def unary(self, request, context):
        if request.message=="game over":
            print("\ngot game over req\n")
            self.game_over=True
        return game_pb2.Response(message="game over")

    def missile_approach(self, request, context):
        
        attack =0
        while( not self.game_over):
            while len(self.missiles) > attack:
                m = self.missiles[attack]
                print(f"attacking with misile {attack} : {m}")
                attack += 1
                yield game_pb2.Missile(x=m.x_cord,y=m.y_cord,rad=m.rad)

        
        
        # x=random.randint(0,10)
        # y=random.randint(0,10)
        # s=random.randint(1,4)
        # m=s1.Missile(x_cord=x,y_cord=y,rad=s)
        # return game_pb2.Missile(x=m.x_cord,y=m.y_cord,rad=m.rad)



	  
def server():
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
   game_pb2_grpc.add_GameServicer_to_server(Game(), server)
   server.add_insecure_port('[::]:50051')
   print("gRPC starting")
   server.start()
   server.wait_for_termination()
server()