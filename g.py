'''
Created on 24 de fev de 2016

@author: fvj
'''
from random import random
from math import sqrt
from copy import deepcopy
import time
import matplotlib.pyplot as plot

G_CONST = 20
NUMBER_OF_BODIES = 20

TOTAL_STEPS = 500
STEP_SIZE = 0.2
SLEEP_TIME = 0

class Body():
    RAND_MASS = 500
    RAND_SPEED = 2
    RAND_POSITION = 800
        
    def __init__(self, mass, x=0, y=0, x_speed=0, y_speed=0):
        self.mass = mass
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.x_acc = 0
        self.y_acc = 0
        self.color = [random(), random(), random()]
    
    @staticmethod
    def getRandomBody():
        mass = Body.RAND_MASS*random()
        x = Body.RAND_POSITION*(1-2*random())
        y = Body.RAND_POSITION*(1-2*random())
        x_speed = Body.RAND_SPEED*(1-2*random())
        y_speed = Body.RAND_SPEED*(1-2*random())
        return Body(mass, x, y, x_speed, y_speed)
        
        
    def step(self, snapshot):
        self.calculateAcceleration(snapshot)
        self.move()
    
    def calculateAcceleration(self, snapshot):
        x_force = 0
        y_force = 0
        
        for body in snapshot:
            delta_x = body.x-self.x
            delta_y = body.y-self.y
            distance = sqrt( delta_x**2 + delta_y**2 )
            if distance == 0: # THIS IS ME! (OR SOMETHING I COLLIDED)
                continue
            force = G_CONST*self.mass*body.mass/(distance**2)
            x_force += force*delta_x/distance
            y_force += force*delta_y/distance
            
        self.x_acc = x_force/self.mass
        self.y_acc = y_force/self.mass
        
    def move(self):
        self.x += self.x_speed*STEP_SIZE + 0.5*self.x_acc*(STEP_SIZE**2)
        self.y += self.y_speed*STEP_SIZE + 0.5*self.y_acc*(STEP_SIZE**2)
        
        self.x_speed += self.x_acc*STEP_SIZE
        self.y_speed += self.y_acc*STEP_SIZE

class Space():
    WIDTH = 1000
    HEIGHT = 1000
    
    def __init__(self):
        self.bodies = []
    
    def addBody(self, body):
        self.bodies.append(body)
        
    def preparePlot(self):
        self.fig, self.ax = plot.subplots(1, 1)
        self.ax.set_aspect('equal')
        self.ax.set_xlim(-self.WIDTH, self.WIDTH)
        self.ax.set_ylim(-self.HEIGHT, self.HEIGHT)
        self.ax.hold(True)
        plot.show(False)
        plot.draw()
        
        self.background = self.fig.canvas.copy_from_bbox(self.ax.bbox)
        
        plot.ion()
        plot.show()
    
        
    def plot(self):
        self.fig.canvas.restore_region(self.background)
        
        for body in self.bodies:
            points = self.ax.plot(body.x, body.y, color=body.color, marker='o', markersize=(body.mass/50))[0]
        
            # redraw just the points
            self.ax.draw_artist(points)

        # fill in the axes rectangle
        self.fig.canvas.blit(self.ax.bbox)
        
    
    def clear_plot(self):
        plot.cla()
    
    def step(self):
        snapshot = deepcopy(self.bodies)
        for body in self.bodies:
            body.step(snapshot)




def setupInitialConditions(self):
    for i in range(NUMBER_OF_BODIES):
        self.addBody(Body.getRandomBody())

#     universe.addBody(Body(700))
#     universe.addBody(Body(180, -250, -250, -4, 5))
#     universe.addBody(Body(180, -250, 250, 3, 4))
#     universe.addBody(Body(60, 420, 420, 3, -2))
#     
#     universe.addBody(Body(400, 0, 0, 0.1, -0.1))
#     universe.addBody(Body(80, 150, 150, 2, -2))
#     universe.addBody(Body(50, -400, 400, 3, 1))


# ============================================================================    

print("starting...")

universe = Space()
# universe.preparePlot()

setupInitialConditions(universe)

start_timestamp = time.time()
for step in range(TOTAL_STEPS):
# while True:
    universe.step()
#     universe.plot()
    time.sleep(SLEEP_TIME)
end_timestamp = time.time()

print("done in {:.2f} seconds!".format(end_timestamp - start_timestamp))