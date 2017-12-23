import numpy as np
import time
from graphics import *

class body:

    def __init__(self,rad,distance,xv,yv,mass):
        self.xpos = np.cos(float(rad))*distance
        self.ypos = np.sin(float(rad))*distance
        self.xvel = float(xv)
        self.yvel = float(yv)
        self.mass = float(mass)
        # Size is a function of mass
        self.radius = np.log10(self.mass)*4
        self.ivel = 0

    def update(self, time):
        # Updates position
        self.xpos = self.xpos + time*self.xvel
        self.ypos = self.ypos + time*self.yvel

    def gravity(self,time, ebody):
        # Updates velocity according to gravitational force
        
        ## G is Gravitational Constant
        G = 6.67408 * (10**-11)

        ## The algorithm of gravity
        rsquared = (ebody.getY()-self.ypos)**2 + (ebody.getX()-self.xpos)**2
        gamma = np.arctan2(ebody.getY()-self.ypos, ebody.getX()-self.xpos)
        acc = ((G * self.mass * ebody.getmass())/rsquared)/self.mass
        xacc = acc * np.cos(gamma)
        yacc = acc * np.sin(gamma)
        self.xvel = self.xvel + xacc*time
        self.yvel = self.yvel + yacc*time

    def getY(self):
        return self.ypos

    def getX(self):
        return self.xpos

    def getYv(self):
        return self.yvel

    def getXv(self):
        return self.xvel

    def getrad(self):
        return self.radius

    def getmass(self):
        return self.mass

def drawer(circlelist,i,colour):
    # Draws the shapes that repersent the planets
    circlelist = circlelist + [Circle(Point(bodies[i].getX(),bodies[i].getY()),bodies[i].getrad())]
    circlelist[i].setFill(colour[i])
    circlelist[i].setOutline(colour[i])
    return circlelist

def setup():
    global bodies
    ## body(degrees from positive x axis assuming coordinates grid on screen,distance,xvel,yvel,mass)
    ## Note: Realistic simulations are very boring due to low speed
    ## sun = body(0,0,0,0,1.989*10**30)
    ## earth = body(0,1.469*10**11,0,460,5.972*10**24)
    bodies = [body(0,0,0,0,1.989*10**30),body(0,2*10**7,0,3000000,5.972*10**24)]

def store(texts,c,i):
    texts[c] = texts[c] + "Run %6.0f" % (i) + " %11.0f" % (bodies[c].getX()) + "m" + " %13.0f" % (bodies[c].getY()) + "m" \
               + " %13.0f" % (bodies[c].getXv()) + "m" + " %12.0f" % (bodies[c].getYv()) + "m" + "\n"
def main():

    setup()

    outfile = open("orbit", "w")

    ## GUI
    ## Changes colour of planets
    colour = ["red","green"]
    win = GraphWin("Orbits", 600, 600)
    win.setCoords(-1*10**8,-1*10**8,1*10**8,1*10**8)
    win.setBackground("black")

    circlelist = []
    for i in range(len(bodies)):
        ## Draws planets for GUI
        circlelist = drawer(circlelist,i,colour)
        circlelist[i].draw(win)

    ## Text storage
    texts = ['']*len(bodies)
    header = "Interval     X Position     Y Position     X velocity    Y velocity"
    ## Interval of recording
    rinterval = 100
    p = rinterval

    ## Simulation interval
    interval = 0.01

    ## Steps up simulation
    ## Runs is amount of steps
    runs = 10000
    for i in range(runs):
        for c in range(len(bodies)):
            for k in range(len(bodies)):
                if k != c:
                    ## Does simulation for each body
                    bodies[c].gravity(interval,bodies[k])

            ## Updates GUI
            circlelist[c].move(bodies[c].getXv()*interval,bodies[c].getYv()*interval)
                    
            ## Draws path (note very laggy)
            ## win.plot(bodies[c].getX(),bodies[c].getY(),colour[c])

            ## Updates position
            bodies[c].update(interval)

            ## Stores information as text
            if (p >=rinterval):
                p = 0
                store(texts,c,i)
            else:
                p = p + 1

    print header
    outfile.write(header + "\n")
    for i in range(len(texts)):
        print "Body" + str(i+1)
        outfile.write("Body" + str(i+1) + "\n")
        print texts[i]
        outfile.write(texts[i] + "\n")
    
    time.sleep(1)
    win.close()

if __name__ == '__main__':
    main()
