'''
Created on 24 de fev de 2016

@author: fvj
'''
from random import random
from math import sqrt
from copy import deepcopy
from time import time
import matplotlib.pyplot as plot
import matplotlib.animation as animation

G_CONST = 1
NUMBER_OF_BODIES = 20
STEP_SIZE = 0.5

class Body():
    RAND_MASS = 5000
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
    def __init__(self):
        self.bodies = []
        self.setupInitialConditions()
    
    def addBody(self, body):
        self.bodies.append(body)
    
    def animate(self):
        plotter = Plotter(self)
        plotter.animate()
        
    def step(self):
        snapshot = deepcopy(self.bodies)
        for body in self.bodies:
            body.step(snapshot)

    def setupInitialConditions(self):
        for _ in range(NUMBER_OF_BODIES):
            self.addBody(Body.getRandomBody())

class Plotter():
    WIDTH = 1000
    HEIGHT = 1000
    
    def __init__(self, space):
        self.universe = space
        self.fig = plot.figure()
        self.ax = plot.axes(xlim=(-self.WIDTH, self.WIDTH), ylim=(-self.HEIGHT, self.HEIGHT))
        for body in self.universe.bodies:
            size = max(body.mass/500, 1)
            points = self.ax.plot(body.x, body.y, color=body.color, marker='o', markersize=size)[0]
            self.ax.add_artist(points)
            
    def initPlot(self):
        for line in self.ax.get_lines():
            line.set_data([], [])
        return self.ax.get_lines()
    
    def plotStep(self, frame):
        self.universe.step()
        
        for i in range(len(self.ax.get_lines())):
            self.ax.get_lines()[i].set_data(self.universe.bodies[i].x, self.universe.bodies[i].y)
        
        return self.ax.get_lines()
            
    def animate(self):
        self.animation = animation.FuncAnimation(self.fig, self.plotStep, init_func=self.initPlot,
           frames=1, interval=1, blit=True)

        plot.show()
# ============================================================================    

print("starting...")

universe = Space()

start_timestamp = time()

universe.animate()

end_timestamp = time()

print("done in {:.1f} seconds!".format(end_timestamp - start_timestamp))