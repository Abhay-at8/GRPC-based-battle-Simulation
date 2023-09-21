class Soldier:

  def __init__(self, x_cord, y_cord, speed, soldierid):
    self.x_cord = x_cord
    self.y_cord = y_cord
    self.speed = speed
    self.alive = True
    self.soldierID =soldierid

  def __str__(self):
    return f'id:{self.soldierID} x: {self.x_cord} y:{self.y_cord} speed{self.speed}'
  
  def in_redzone(self, missile):
    return (missile.left_bdry <= self.x_cord <= missile.right_bdry and \
            missile.bottom_bdry >= self.y_cord >= missile.top_bdry)
  
  def take_shelter(self, missile, N):
    #print(missile.right_bdry)
    if self.in_redzone(missile):
      
      if missile.right_bdry < (self.x_cord + self.speed) < N:
        str=f'Soldier {self.soldierID} moved right by {self.speed} from ({self.x_cord},{self.y_cord}) to '
        self.x_cord = self.x_cord + self.speed
        str+=f'({self.x_cord},{self.y_cord})\n'
        
      elif 0 < (self.x_cord - self.speed) < missile.left_bdry:
        str=f'Soldier {self.soldierID} moved left by {self.speed} from ({self.x_cord},{self.y_cord}) to '
        self.x_cord = self.x_cord - self.speed
        str+=f'({self.x_cord},{self.y_cord})\n'
      elif 0 < self.y_cord - self.speed <= missile.top_bdry:
        str=f'Soldier {self.soldierID} moved backwards by {self.speed} from ({self.x_cord},{self.y_cord}) to '
        self.y_cord = self.y_cord - self.speed
        str+=f'({self.x_cord},{self.y_cord})\n'
      elif missile.bottom_bdry < self.y_cord + self.speed < N:
        str=f'Soldier {self.soldierID} moved forward by {self.speed} from ({self.x_cord},{self.y_cord}) to '
        self.y_cord = self.y_cord + self.speed
        str+=f'({self.x_cord},{self.y_cord})\n'
      else:
        str=f'Soldier {self.soldierID} died \n'
        self.alive = False
    else:
      str=f'Soldier {self.soldierID} out of red zone \n'
    return str


def was_hit(soldierID, trueFlag):
  # check if any soldier is alive and has the same ID
  if any(soldier.soldierID == soldierID and soldier.alive for soldier in arr):
    trueFlag = 1
  # check if any soldier is dead and has the same ID
  elif any(soldier.soldierID == soldierID and not soldier.alive
           for soldier in arr):
    trueFlag = 0
  else:
    print("Not a valid soldier id")

  


class Missile:

  def __init__(self, x_cord, y_cord, rad):
    self.x_cord = x_cord
    self.y_cord = y_cord
    self.rad = rad

    # missile impact radius boundaries
    self.left_bdry = self.x_cord - self.rad
    self.right_bdry = self.x_cord + self.rad
    self.top_bdry = self.y_cord - self.rad
    self.bottom_bdry = self.y_cord + self.rad
    #out of field condn
    '''if(self.bottom_bdry>N or self.right_bdry>N):
      self.right_bdry=self.bottom_bdry=N
    if (self.left_bdry<0 or self.top_bdry<0 ):
      self.top_bdry=self.left_bdry=0'''
    
    #print(self.right_bdry,self.left_bdry,self.top_bdry, self.bottom_bdry)

  def __str__(self):
       return f' x: {self.x_cord} y:{self.y_cord} speed{self.rad}'
 
