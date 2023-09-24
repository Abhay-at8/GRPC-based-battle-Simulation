class Soldier:

    def __init__(self, x_cord, y_cord, speed, soldierid):
        """ Initializes a new soldier object.

            Args:
                x_cord: The soldier's initial x-coordinate. This is the soldier's position on the battlefield.
                y_cord: The soldier's initial y-coordinate. This is the soldier's position on the battlefield.
                speed: The soldier's speed. This is how far the soldier can move in one time step.
                soldierid: The soldier's ID. This is a unique identifier for the soldier.
        """

        self.x_cord = x_cord
        self.y_cord = y_cord
        self.speed = speed
        self.alive = True
        self.soldierID = soldierid

    def __str__(self):
        """ Returns a string representation of the soldier object.

            Returns: A string representation of the soldier object. This string includes the soldier's ID,
            x-coordinate, y-coordinate, and speed.
        """
        # f'Soldier with ID: {self.soldierID} at (x:{self.x_cord},y:{self.y_cord}) with speed:{self.speed}'
        soldier_string = f'Soldier ID: {self.soldierID} \nInitial Position: (x:{self.x_cord},y:{self.y_cord})\nSpeed:{self.speed} '
        return soldier_string

    # checking if a soldier is in redzone after a missile approach
    def in_redzone(self, missile):
        """ Checks if the soldier is in the red zone of the missile.

         Args:
             missile: The missile object.

         Returns:
             True if the soldier is in the red zone of the missile, False otherwise.
         """

        return missile.left_bdry <= self.x_cord <= missile.right_bdry and missile.bottom_bdry >= self.y_cord >= missile.top_bdry

    # soldier movement after a missile approach based on its position
    def take_shelter(self, missile, N):
        """ Takes shelter from the missile.

          Args:
              missile: The missile object.
              N: The battlefield matrix size.

          Returns:
              A string message indicating whether the soldier was able to take shelter successfully or not.
        """
        # if soldier in the red zone change the soldier coordinates and record soldier movement
        if self.in_redzone(missile):
            # Move the soldier in a safe direction, if possible.
            if missile.right_bdry < (self.x_cord + self.speed) < N:
                soldier_movement = f'Soldier {self.soldierID} moved right by {self.speed} from ({self.x_cord},{self.y_cord}) to '
                self.x_cord = self.x_cord + self.speed
                soldier_movement += f'({self.x_cord},{self.y_cord})\n'
            elif 0 < (self.x_cord - self.speed) < missile.left_bdry:
                soldier_movement = f'Soldier {self.soldierID} moved left by {self.speed} from ({self.x_cord},{self.y_cord}) to '
                self.x_cord = self.x_cord - self.speed
                soldier_movement += f'({self.x_cord},{self.y_cord})\n'
            elif 0 < self.y_cord - self.speed < missile.top_bdry:
                soldier_movement = f'Soldier {self.soldierID} moved backwards by {self.speed} from ({self.x_cord},{self.y_cord}) to '
                self.y_cord = self.y_cord - self.speed
                soldier_movement += f'({self.x_cord},{self.y_cord})\n'
            elif missile.bottom_bdry < self.y_cord + self.speed < N:
                soldier_movement = f'Soldier {self.soldierID} moved forward by {self.speed} from ({self.x_cord},{self.y_cord}) to '
                self.y_cord = self.y_cord + self.speed
                soldier_movement += f'({self.x_cord},{self.y_cord})\n'
            else:
                # The soldier cannot move to safe location before missile hit, so it dies.
                soldier_movement = f'Soldier {self.soldierID} died \n'
                self.alive = False

        else:
            # The soldier is already out of the red zone.
            soldier_movement = f'Soldier {self.soldierID} out of red zone. \n'
        return soldier_movement


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
        """ Initializes a new missile object.

                 Args:
                     x_cord: The missile's initial x-coordinate. This is the missile's position on the battlefield.
                     y_cord: The missile's initial y-coordinate. This is the missile's position on the battlefield.
                     rad: The missile's radius. This is the size of the missile's explosion zone.
        """

        self.x_cord = x_cord
        self.y_cord = y_cord
        self.rad = rad

        # Calculate the missile's red zone. This is the area around the missile that will be affected by the explosion.
        self.left_bdry = self.x_cord - self.rad
        self.right_bdry = self.x_cord + self.rad
        self.top_bdry = self.y_cord - self.rad
        self.bottom_bdry = self.y_cord + self.rad

    def __str__(self):
        """Returns a string representation of the missile object.

                Returns: A string representation of the missile object. This string includes the missile's
                x-coordinate, y-coordinate, and radius.
        """
        return f'at ({self.x_cord},{self.y_cord}) of radius {self.rad}'
