# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent

class MyAI ( Agent ):

    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        self.CurrentLocation = [1,1]
        self.facing = "up"
        self.GotGold = False
        self.SafeLocations = []
        self.backtrack = False
        self.BackOne = False
        self.start = False
        self.Destinations = []
        self.Warnings = []
        self.PossibleDangers = []
        self.Boundary = []
        self.trigger = True
        self.History = []
        self.BumpPhen = False
        self.BackEmpty = False
        self.DeadWumpus = False
        self.ShotArrow = False
        self.WumpusLocation = [0,0]
        self.counter = 0
        
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        # print()
        # print("Current Location: ",self.CurrentLocation)
        # print("Facing: ", self.facing)
        # print("safe locations: ",self.SafeLocations)
        # print("Warnings Locations", self.Warnings)
        # print("Possible Dangers", self.PossibleDangers)
        # print("Boundary: ", self.Boundary)
        
        # print("History",self.History)
        self.History.append(self.CurrentLocation)
        #Our Agent dips if the first square has the gold
        # or if the squares have a breeze or a stench
        # thats because there is a 50% chance the next square is a pit or a wumpus


        self.counter+=1

        if self.counter == 100:
            self.backtrack = True
            #print('NOT WORTH IT')
            return self.BackTrackSequence()


        if self.CurrentLocation == [1,1]:
            for i in self.Destinations:
                if i[0] == self.CurrentLocation[0] and i[1] == self.CurrentLocation[1]:
                    self.Destinations.remove(i)
        if len(self.Destinations) > 0 and len(self.Destinations) != 1:
            for i in self.Destinations:
                if i[0] == self.CurrentLocation[0] and i[1] == self.CurrentLocation[1]:
                    self.Destinations.remove(i)
        if self.BackEmpty == True:
            for i in self.Destinations:
                if i[0] == self.CurrentLocation[0] and i[1] == self.CurrentLocation[1]:
                    self.Destinations.remove(i)
            
        #print("CDest", self.Destinations)
        if self.start == False:
            if self.facing == "up":
                self.start = True
                return Agent.Action.TURN_LEFT
            if self.facing == "right":
                self.start = True
        
        if self.CurrentLocation == [1,1]:
            if glitter:
                #print("First Glitter")
                self.backtrack = True
                return Agent.Action.GRAB
            if breeze == True:
                #print("First Breeze")
                return Agent.Action.CLIMB
            if scream == True:
                self.DeadWumpus = True
                self.FutureDestinations()
                #print("Dest", self.Destinations)
                if self.CurrentLocation not in self.SafeLocations:
                    self.SafeLocations.append(self.CurrentLocation)
                
                #print("Going Forward1")
                return self.MoveToLocation()
            if stench == True:
                if self.ShotArrow == True and self.DeadWumpus == False:
                    #print("First Stench1")
                    
                    return Agent.Action.CLIMB
                if self.ShotArrow == True and self.DeadWumpus == True:
                    #print("First Stench1")
                    return Agent.Action.CLIMB
                else:
                    #print("First Stench")
                    self.ShotArrow = True
                    return Agent.Action.SHOOT

            
            

            
        if self.trigger == False and len(self.Destinations) == 0:
            return self.BackTrackSequence()
        else:
            # IF there is glitter than turn on the backtracking sequence so we can go home
            if glitter == True:
                #print("***********Glit here**************")
                self.backtrack = True
                self.GotGold = True
                return Agent.Action.GRAB
            
            if self.backtrack == True:
                return self.BackTrackSequence()

            if self.BackOne == True:
                return self.BackTrackOne()
                
            #we didnt shoot an arrow and the wumpus isnt dead
            if stench == True and self.DeadWumpus == False and self.ShotArrow == False:      
                #print("stench")
                #Add the stench to the lsit of Warnings
                self.Warnings.append(self.CurrentLocation)
                self.AddPresumptions()
                self.ShotArrow = True
                return Agent.Action.SHOOT
            #we shot the arrow and the wumpus is dead
            #do nothing

            #we shot the arrow and the wumpus isnt dead
            if stench == True and self.DeadWumpus == False and self.ShotArrow == True and self.WumpusLocation == [0,0]:
                self.Warnings.append(self.CurrentLocation)
                self.AddPresumptions()
                #self.WumpusCord()
                return self.BackTrackOne()
            
            if breeze == True:
                #print("breeze")
                #add the breeze to the list of Warningss
                self.Warnings.append(self.CurrentLocation)
                self.AddPresumptions()
                return self.BackTrackOne()

            if bump == True:
                self.BumpPhen = True
                self.BackEmpty = True
                #print("bump")
                self.Boundary.append(self.CurrentLocation)
                self.UpdateCurrentLocation()
                return self.MoveToLocation()
                
            if self.DeadWumpus == True:
                if not breeze and not glitter and not bump:
                    self.FutureDestinations()
                    #print("Dest", self.Destinations)
                    if self.CurrentLocation not in self.SafeLocations:
                        self.SafeLocations.append(self.CurrentLocation)
                    
                    #print("Going Forward1")
                    return self.MoveToLocation()
            if self.DeadWumpus == False:   
                if not stench and not breeze and not glitter and not bump:
                    self.FutureDestinations()
                    #print("Dest", self.Destinations)
                    if self.CurrentLocation not in self.SafeLocations:
                        self.SafeLocations.append(self.CurrentLocation)
                    
                    #print("Going Forward1")
                    return self.MoveToLocation()
            
        
            return Agent.Action.CLIMB
        
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================

    def WumpusCord(self):
        if self.facing == "up":
            temp1 = [self.CurrentLocation[0],self.CurrentLocation[1]]
            temp1[0] = temp1[0]+1
            WumpusLocation = temp1
        if self.facing == "right":
            temp1 = [self.CurrentLocation[0],self.CurrentLocation[1]]
            temp1[1] = temp1[1]+1
            WumpusLocation = temp1
    def AddPresumptions(self):
        temp1 = [self.Warnings[-1][0],self.Warnings[-1][1]]
        temp2 = [self.Warnings[-1][0],self.Warnings[-1][1]]
        temp1[0] = temp1[0]+1
        temp2[1] = temp2[1]+1
        self.PossibleDangers.append(temp2)
        self.PossibleDangers.append(temp1)
    
    def MoveToLocation(self):
        if self.BackEmpty == True:
            for i in self.Destinations:
                if i[0] == self.CurrentLocation[0] and i[1] == self.CurrentLocation[1]:
                    self.Destinations.remove(i)
                    self.BackEmpty = False
        if self.facing == "right" and len(self.Destinations) != 0:
            #the destination is down
            if self.Destinations[-1][0] == (self.CurrentLocation[0] - 1) and self.Destinations[-1][1] == self.CurrentLocation[1]:
                self.facing = "down"
                return Agent.Action.TURN_RIGHT

            #its on left
            elif self.Destinations[-1][0] == self.CurrentLocation[0] and self.Destinations[-1][1] == (self.CurrentLocation[1] - 1):
                self.facing = "up"
                return Agent.Action.TURN_LEFT

            #its on top
            elif self.Destinations[-1][0] == (self.CurrentLocation[0] + 1) and self.Destinations[-1][1] == self.CurrentLocation[1]:
                self.facing = "up"
                return Agent.Action.TURN_LEFT

            #its on the right
            elif self.Destinations[-1][0] == self.CurrentLocation[0] and self.Destinations[-1][1] == (self.CurrentLocation[1]+1):
                self.facing = "right"
                self.UpdateCurrentLocation()
                return Agent.Action.FORWARD
            else:
                #print("we in here")
                self.SafeLocations.pop(-1)
                return self.BackTrackOne()

        elif self.facing == "up" and len(self.Destinations) != 0:
            #the destination is down
            if self.Destinations[-1][0] == (self.CurrentLocation[0] - 1) and self.Destinations[-1][1] == self.CurrentLocation[1]:
                self.facing = "right"
                return Agent.Action.TURN_RIGHT

            #its on left
            elif self.Destinations[-1][0] == self.CurrentLocation[0] and self.Destinations[-1][1] == (self.CurrentLocation[1] - 1):
                self.facing = "left"
                return Agent.Action.TURN_LEFT

            #its on top
            elif self.Destinations[-1][0] == (self.CurrentLocation[0] + 1) and self.Destinations[-1][1] == self.CurrentLocation[1]:
                self.facing = "up"
                self.UpdateCurrentLocation()
                return Agent.Action.FORWARD

            #its on the right
            elif self.Destinations[-1][0] == self.CurrentLocation[0] and self.Destinations[-1][1] == (self.CurrentLocation[1]+1):
                self.facing = "right"
                return Agent.Action.TURN_RIGHT
            else:
                #print("we in here")
                self.SafeLocations.pop(-1)
                return self.BackTrackOne()

        elif self.facing == "down" and len(self.Destinations) != 0:
            #the destination is down
            #print("mellooooo")
            if self.Destinations[-1][0] == (self.CurrentLocation[0] - 1) and self.Destinations[-1][1] == self.CurrentLocation[1]:
                #print("melow 3")
                self.facing = "down"
                self.UpdateCurrentLocation()
                return Agent.Action.FORWARD

            #its on left
            elif self.Destinations[-1][0] == self.CurrentLocation[0] and self.Destinations[-1][1] == (self.CurrentLocation[1] - 1):
                self.facing = "left"
                return Agent.Action.TURN_RIGHT

            #its on top
            elif self.Destinations[-1][0] == (self.CurrentLocation[0] + 1) and self.Destinations[-1][1] == self.CurrentLocation[1]:
                self.facing = "left"
                return Agent.Action.TURN_RIGHT

            #its on the right
            elif self.Destinations[-1][0] == self.CurrentLocation[0] and self.Destinations[-1][1] == (self.CurrentLocation[1]+1):
                self.facing = "right"
                return Agent.Action.TURN_LEFT
            else:
                #print("we in here")
                self.SafeLocations.pop(-1)
                return self.BackTrackOne()
            
        elif self.facing == "left" and len(self.Destinations) != 0:
            #the destination is down
            if self.Destinations[-1][0] == (self.CurrentLocation[0] - 1) and self.Destinations[-1][1] == self.CurrentLocation[1]:
                self.facing = "down"
                return Agent.Action.TURN_LEFT

            #its on left
            elif self.Destinations[-1][0] == self.CurrentLocation[0] and self.Destinations[-1][1] == (self.CurrentLocation[1] - 1):
                self.facing = "left"
                self.UpdateCurrentLocation()
                return Agent.Action.FORWARD

            #its on top
            elif self.Destinations[-1][0] == (self.CurrentLocation[0] + 1) and self.Destinations[-1][1] == self.CurrentLocation[1]:
                self.facing = "up"
                return Agent.Action.TURN_RIGHT

            #its on the right
            elif self.Destinations[-1][0] == self.CurrentLocation[0] and self.Destinations[-1][1] == (self.CurrentLocation[1]+1):
                self.facing = "up"
                return Agent.Action.TURN_RIGHT
            else:
                #print("we in here")
                self.SafeLocations.pop(-1)
                return self.BackTrackOne()
        else:
            #print("we in here")
            self.SafeLocations.pop(-1)
            return self.BackTrackOne()            

            
    def FutureDestinations(self):
        self.trigger = False
        temp1 = [self.CurrentLocation[0],self.CurrentLocation[1]]
        temp2 = [self.CurrentLocation[0],self.CurrentLocation[1]]
        temp1[0] = temp1[0]+1
        temp2[1] = temp2[1]+1
        if temp2 not in self.Warnings and temp2 not in self.Destinations and temp2 not in self.Boundary and temp2 not in self.History:
            self.Destinations.append(temp2)
        if temp1 not in self.Warnings and temp1 not in self.Destinations and temp1 not in self.Boundary and temp1 not in self.History:
            self.Destinations.append(temp1)
        
    def UpdateCurrentLocation(self):
        if self.BumpPhen == False:
            if self.facing == "right":
                self.CurrentLocation = [self.CurrentLocation[0],self.CurrentLocation[1] + 1]
            if self.facing == "left":
                self.CurrentLocation = [self.CurrentLocation[0],self.CurrentLocation[1] - 1]
            if self.facing == "up":
                self.CurrentLocation = [self.CurrentLocation[0] + 1,self.CurrentLocation[1]]
            if self.facing == "down":
                 self.CurrentLocation = [self.CurrentLocation[0] - 1,self.CurrentLocation[1]]
        else:
            self.BumpPhen = False
            if self.facing == "right":
                self.CurrentLocation = [self.CurrentLocation[0],self.CurrentLocation[1] - 1]
            if self.facing == "left":
                self.CurrentLocation = [self.CurrentLocation[0],self.CurrentLocation[1] + 1]
            if self.facing == "up":
                self.CurrentLocation = [self.CurrentLocation[0] - 1,self.CurrentLocation[1]]
            if self.facing == "down":
                 self.CurrentLocation = [self.CurrentLocation[0] -+1,self.CurrentLocation[1]]
            

    def BackTrackSequence(self):
        #print("========Starting Backtracking======")
        self.backtrack = True
        if self.CurrentLocation == [1,1]:
            #print("End Game")
            #print(self.DeadWumpus)
            return Agent.Action.CLIMB
        else:
            #GO Left
            
            if self.SafeLocations[-1] != [1,1] and self.SafeLocations[-1] == self.CurrentLocation:
                self.SafeLocations.pop(-1)
            #print("Back safe locations: ",self.SafeLocations)
            if (self.SafeLocations[-1][1] < self.CurrentLocation[1]):
                if self.facing == "right":
                    self.facing = "up"
                    return Agent.Action.TURN_LEFT
                if self.facing == "up":
                    self.facing = "left";
                    return Agent.Action.TURN_LEFT
                if self.facing == "down":
                    self.facing = "left"
                    return Agent.Action.TURN_RIGHT
                if self.facing == "left":
                    
                    self.UpdateCurrentLocation()
                    #print("Going Forward")
                    return Agent.Action.FORWARD
            #GoDown
            if (self.SafeLocations[-1][0] < self.CurrentLocation[0]):
                if self.facing == "up":
                    self.facing = "left"
                    return Agent.Action.TURN_LEFT
                if self.facing == "left":
                    self.facing = "down";
                    return Agent.Action.TURN_LEFT
                if self.facing == "down":
                
                    self.UpdateCurrentLocation()
                    #print("Going Forward")
                    return Agent.Action.FORWARD
            #to go up
            if (self.SafeLocations[-1][0] > self.CurrentLocation[0] and self.SafeLocations[-1][1] == self.CurrentLocation[1]):
                if self.facing == "right":
                    #its on top
                    self.facing = "up"
                    return Agent.Action.TURN_LEFT
                if self.facing == "up":
                    #its on top
                    self.facing = "up"
                    self.UpdateCurrentLocation()
                    return Agent.Action.FORWARD
                if self.facing == "down":
                    #its on top
                    self.facing = "left"
                    return Agent.Action.TURN_RIGHT
                if self.facing == "left":
                    #its on top
                    self.facing = "up"
                    return Agent.Action.TURN_RIGHT

    def BackTrackOne(self):
        if len(self.Destinations) == 1:
            self.BackEmpty = True
        #print("========Going Back One======")
        #print("One safe locations: ",self.SafeLocations)
        #GoLeft
        if self.CurrentLocation == self.SafeLocations[-1]:
            self.SafeLocations.pop(-1)
            
        if (self.SafeLocations[-1][1] < self.CurrentLocation[1]):
            if self.facing == "right":
                self.facing = "up"
                return Agent.Action.TURN_LEFT
            if self.facing == "up":
                self.facing = "left";
                return Agent.Action.TURN_LEFT
            if self.facing == "left":
                self.UpdateCurrentLocation()
                #print("Going Forward")
                self.BackOne = False
                self.BackEmpty = False
                return Agent.Action.FORWARD
        #GoDown
        if (self.SafeLocations[-1][0] < self.CurrentLocation[0] and self.SafeLocations[-1][1] == self.CurrentLocation[1]):
            if self.facing == "up":
                self.facing = "left"
                return Agent.Action.TURN_LEFT
            if self.facing == "left":
                self.facing = "down"
                return Agent.Action.TURN_LEFT
            if self.facing == "right":
                self.facing = "down"
                return Agent.Action.TURN_RIGHT
            if self.facing == "down":
                self.UpdateCurrentLocation()
                #print("Going Forward")
                self.BackOne = False
                self.BackEmpty = False
                return Agent.Action.FORWARD
        #GOUp
        if(self.SafeLocations[-1][0] > self.CurrentLocation[0] and self.SafeLocations[-1][1] == self.CurrentLocation[1]):
            #print("ninnnnnnnnneeeew")
            if self.facing == "up":
                self.facing = "up"
                self.UpdateCurrentLocation()
                #print("Going Forward")
                self.BackOne = False
                self.BackEmpty = False
                return Agent.Action.FORWARD   
            if self.facing == "left":
                self.facing = "up"
                return Agent.Action.TURN_RIGHT
            if self.facing == "down":
                self.facing = "left"
                return Agent.Action.TURN_RIGHT
            if self.facing == "right":
                self.facing = "up"
                return Agent.Action.TURN_LEFT
                
         

            
        
    
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================

