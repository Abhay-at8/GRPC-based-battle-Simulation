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
        self.t=0


    soldierId=0
    soldiers=[]

    def status_all(self, request, context):
        msg="\n"
        for soldier in self.soldiers:
            #print(f"before: {soldier}\n")
            msg+=f"soldier Id : {soldier.soldierID}"
            
            if soldier.alive:
                msg+=", status : alive\n"
            else:
                msg+=", status : dead\n"
            #     self.soldiers.remove(soldier)
        return  game_pb2.Response(message=msg)

    def update_cordinates(self, request, context):
        #print(f"\nupdates recieved {request}\n")
        print(request.message)
        for soldier in self.soldiers:
            #print(f"before: {soldier}\n")
            if soldier.soldierID==request.soldierID:
                if request.alive==True:
                    soldier.x_cord=request.x
                    soldier.y_cord=request.x
                else:
                    soldier.alive=False
            #print(f"after: {soldier}\n\n")

        return game_pb2.Empty()


    def register(self, request, context):
        self.soldierId+=1;
        sol_id=self.soldierId
        sol=s1.Soldier(request.x,request.y,request.speed,self.soldierId)
        self.soldiers.append(sol)
        print(f"Registered a soldier {sol_id}\n")
        #print(sol_id)
        print(f"Got request {request}\n" )
        time.sleep(2)
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
        print(f"Incoming missile {self.t}: {m}\n")
        self.t+=1
        if(self.t==4):
            time.sleep(5)
            self.game_over=True
        return game_pb2.Empty()

    
    def unary(self, request, context):
        #if request.message=="game over":
            #print("\ngot game over req\n")
        self.game_over=True
        return game_pb2.Response(message="game over")

    def missile_approach(self, request, context):
        #print(f"attacking with misile\n")
        attack =0
        while( not self.game_over):
            while len(self.missiles) > attack:
                m = self.missiles[attack]
                #print(f"attacking with misile {attack} : {m}")
                attack += 1
                yield game_pb2.Missile(x=m.x_cord,y=m.y_cord,rad=m.rad)
        #print(f"missile attack over")


        


	  
def server():
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
   game_pb2_grpc.add_GameServicer_to_server(Game(), server)
   server.add_insecure_port('[::]:50051')
   print("gRPC starting")
   server.start()
   server.wait_for_termination()
server()