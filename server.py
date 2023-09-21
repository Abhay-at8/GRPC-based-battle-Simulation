from concurrent import futures

import grpc
import game_pb2
import game_pb2_grpc
import Soldier as s1
import time,random
import sys


class Game(game_pb2_grpc.GameServicer):
    def __init__(self):
    # a list to store the connected clients
        self.clients = []
        self.missiles=[]
        self.dead_soldiers=[]
        self.game_over=False
        self.t=0
        self.N=int(sys.argv[1]) #Battlefield Matrix size
        self.M=int(sys.argv[2]) #No of soldiers along with commander
        self.T=int(sys.argv[3]) #Time (No of iteration)


    soldierId=0
    soldiers=[]

    def game_status(self, request, context):
        
        if len(self.soldiers)>=0.5*self.M:
            msg=f"{len(self.soldiers)} out of {self.M} are alive.Game is Won!!!!"
        else:
            msg=f"only {len(self.soldiers)} out of {self.M} are alive. game is lost :("

        print(msg)
        return game_pb2.Response(message=msg)

    def initiaze(self, request, context):
        return game_pb2.InitialValues(sol_id=1,N=self.N,M=self.M,T=self.T)

    def status_all(self, request, context):
        msg="\n"
        for soldier in self.soldiers:
            #print(f"before: {soldier}\n")
            msg+=f"soldier Id : {soldier.soldierID}"
            
            if soldier.alive:
                msg+=", status : alive\n"
            else:
                msg+=", status : dead\n"
                self.dead_soldiers.append(soldier)
                self.soldiers.remove(soldier)
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
        self.soldierId+=1
        sol_id=self.soldierId
        sol=s1.Soldier(request.x,request.y,request.speed,self.soldierId)
        self.soldiers.append(sol)
        print(f"Registered soldier {sol_id}\n")
        #print(sol_id)
        #print(f"Got request {request}\n" )
        time.sleep(2)
        # while True:
        #     if(len(self.soldiers)==3):
        #         break
        return game_pb2.ServerOutput(message='{0}'.format(self.soldierId))
    
    
    def sendMissile(self, request, context):
        #print(f"No of participants:{self.M}")
        while True:
            if(len(self.soldiers)+len(self.dead_soldiers)==self.M):
                break

        time.sleep(5)
        x=random.randint(0,self.N)
        y=random.randint(0,self.N)
        s=random.randint(1,4)
        m=s1.Missile(x_cord=x,y_cord=y,rad=s)
        self.missiles.append(m)
        #print(f"Incoming missile {self.t}: {m}\n")
        self.t+=1
        if(self.t==self.T):
            time.sleep(5)
            self.game_over=True
        return game_pb2.Empty()

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

    def print_layout(self, request, context):
        N=self.N
        missile=self.missiles[self.t-1]
        print(f"at iteration {self.t -1} missile: {missile} \n")
        soldierSet = {(soldier.x_cord, soldier.y_cord) for soldier in self.soldiers}
        print(soldierSet)
        obj_map={}
        for soldier in self.soldiers:
            obj_map[(soldier.x_cord, soldier.y_cord)]=soldier.soldierID
            
        # create the matrix using list comprehension
        mat = [[obj_map[(x, y)] if (x, y) in soldierSet else '.' for x in range(N)]
                for y in range(N)]
        for i in range(N):
            for j in range(N):
                if((i==missile.top_bdry or i==missile.bottom_bdry )):
                    if missile.left_bdry<=j<=missile.right_bdry and mat[i][j]=='.':
                        mat[i][j]='#'
                if(j==missile.right_bdry or j== missile.left_bdry):
                    if(missile.bottom_bdry >=i>=missile.top_bdry) and mat[i][j]=='.':
                        mat[i][j]='#'
        
        #print(mat)
        # print the matrix row by row
        msg="\n"
        for row in mat:
            print(*row)
            for i in row:
                msg+=f"{str(i)} "
            msg+="\n"
        print('\n\n')


        return game_pb2.Request(message=msg)


        


	  
def server():
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
   game_pb2_grpc.add_GameServicer_to_server(Game(), server)
   server.add_insecure_port('[::]:50051')
   print("gRPC starting")
   server.start()
   server.wait_for_termination()
server()