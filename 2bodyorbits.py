
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# gravitational constant
G = 6.67408 * 10**(-11)

class CoordinateMeta(type):
    pass

class Coordinate(metaclass=CoordinateMeta):
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z


    def distance(self, other):
        '''
        distance between this coordinate
        and another coordinate
        '''
        return ( (self.x - other.x)**2
               + (self.y - other.y)**2 
               + (self.z - other.z)**2 )**(1/2)


    def vector(self, other):
        '''
        vector pointing from self
        to other coordinate
        '''
        vec = Coordinate()
        vec.x = other.x - self.x
        vec.y = other.y - self.y
        vec.z = other.z - self.z
        return vec


    def magnitude(self):
        '''
        return the magnitude of self
        '''
        return ( (self.x)**2
               + (self.y)**2
               + (self.z)**2)**(1/2)


    def copy(self):
        '''
        returns a copy of self
        '''
        return Coordinate(self.x, self.y, self.z)


    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'


    def __mul__(self, val):
        x = self.x * val
        y = self.y * val
        z = self.z * val
        return Coordinate(x,y,z)
        

    def __rmul__(self, val):
        return self.__mul__(val)


    def __add__(self, val):
        if type(val) is Coordinate:
            x = self.x + val.x
            y = self.y + val.y
            z = self.z + val.z
        else:
            x = self.x + val
            y = self.y + val
            z = self.z + val
        return Coordinate(x,y,z)


    def __div__(self, val):
        x = self.x / val
        y = self.y / val
        z = self.z / val
        return Coordinate(x,y,z)


    def __truediv__(self, val):
        return self.__div__(val)


    def __rdiv__(self, val):
        x = val / self.x
        y = val / self.y
        z = val / self.z
        return Coordinate(x,y,z)


    def __neg__(self):
        x = -self.x
        y = -self.y
        z = -self.z
        return Coordinate(x,y,z)



class Body:
    def __init__(self, mass):
        self.mass = mass
        self.pos = Coordinate(0,0,0)
        self.vel = Coordinate(0,0,0)
        self.acc = Coordinate(0,0,0)

        # histories
        self.posh: Coordinate = []
        self.velh: Coordinate = []
        self.acch: Coordinate = []


def orbit_calc_2D(body1, body2, t_delta):
    '''
    computes the new positions of two bodies orbiting each other
    adds the new coordinates to the body's position/velocity/acceleration history
    '''
    
    # add the current position to the history
    body1.posh.append(body1.pos.copy())
    body1.velh.append(body1.vel.copy())
    body1.acch.append(body1.acc.copy())

    body2.posh.append(body2.pos.copy())
    body2.velh.append(body2.vel.copy())
    body2.acch.append(body2.acc.copy())

    # distance between bodies
    r = body1.pos.distance(body2.pos)

    # vector from body1 to body2
    rvec = body1.pos.vector(body2.pos)
    rvec = rvec / rvec.magnitude()

    # compute new position and velocity
    body1.pos += body1.vel * t_delta
    body1.vel += body1.acc * t_delta

    body2.pos += body2.vel * t_delta
    body2.vel += body2.acc * t_delta

    # accelerations
    body1.acc = rvec * ( G * body2.mass / (r**2) )
    body2.acc = -rvec * ( G * body1.mass / (r**2) )


def animate_body(body1, body2, t_delta):
    '''
    plots the body movement
    '''

    fig, ax = plt.subplots()

    x1 = [i.x for i in body1.posh]
    y1 = [i.y for i in body1.posh]

    x2 = [i.x for i in body2.posh]
    y2 = [i.y for i in body2.posh]

    frames = np.arange(0, len(x1), 1)

    line1, = ax.plot(x1, y1, 'bo')
    line2, = ax.plot(x2, y2, 'ro')

    trace1, = ax.plot(x1, y1, 'b--')
    trace2, = ax.plot(x2, y2, 'r--')

    ax.axis('equal')

    #plt.show()
    
    #ax.set_xlim(np.min([x1, x2])-1000, np.max([x1,x2])+1000)
    #ax.set_ylim(np.min([y1, y2])-1000, np.max([y1,y2])+1000)


    def animate(frame, line1, line2, trace1, trace2, x1, y1, x2, y2):
        line1.set_xdata(x1[frame])
        line1.set_ydata(y1[frame])

        line2.set_xdata(x2[frame])
        line2.set_ydata(y2[frame])

        trace1.set_xdata(x1[:frame])
        trace1.set_ydata(y1[:frame])

        trace2.set_xdata(x2[:frame])
        trace2.set_ydata(y2[:frame])
        return line1, line2, trace1, trace2


    ani = animation.FuncAnimation(
        fig=fig, func=animate, fargs=(line1,line2,trace1,trace2,x1,y1,x2,y2), frames=frames,
        interval=1, blit=True, save_count=100)

    #writer = animation.ImageMagickWriter(fps=15)
    #ani.save('example.html', 'ImageMagickWriter')

    plt.show()


def animate_body_realtime(body1, body2):

    fig, ax = plt.subplots()
    line1, = ax.plot(0, 0, marker='o', color='b')
    line2, = ax.plot(1, 1, marker='o', color='r')
    trace1, = ax.plot(0, 0, 'b--')
    trace2, = ax.plot(1, 1, 'r--')

    ax.set_xlim(-400 * 10**6, 400 * 10**6)
    ax.set_ylim(-400 * 10**6, 400 * 10**6)

    #ax.set_xlim(np.min([body1.pos.x, body2.pos.x])-100000, np.max([body1.pos.x, body2.pos.x])+100000)
    #ax.set_ylim(np.min([body1.pos.y, body2.pos.y])-100000, np.max([body1.pos.y, body2.pos.y])+100000)

    #ax.set_aspect('equal', 'box')


    def animate(frame, line1, line2, body1, body2):

        orbit_calc_2D(body1, body2, 3600)

        line1.set_xdata(body1.pos.x)
        line1.set_ydata(body1.pos.y)

        line2.set_xdata(body2.pos.x)
        line2.set_ydata(body2.pos.y)

        body1trace = body1.posh[:frame]
        body2trace = body2.posh[:frame]

        trace1.set_xdata([pos.x for pos in body1trace])
        trace1.set_ydata([pos.y for pos in body1trace])

        trace2.set_xdata([pos.x for pos in body2trace])
        trace2.set_ydata([pos.y for pos in body2trace])

        #line1.axes.set_aspect('equal')
        
        return line1, line2, trace1, trace2


    ani = animation.FuncAnimation(
        fig=fig, func=animate, fargs=(line1,line2,body1,body2), interval=2, save_count=50, blit=True)

    plt.show()

    



def main():

    body1 = Body(mass=6 * 10**24)
    body1.pos = Coordinate(0,0)
    body1.vel = Coordinate(0,0)

    body2 = Body(mass=7 * 10**23)
    body2.pos = Coordinate(360*10**6,0)
    body2.vel = Coordinate(0,1000)

    t_delta = 5000

    #animate_body_realtime(body1, body2)

    times = np.arange(0, 10000000, t_delta)
    for t in times:
        orbit_calc_2D(body1, body2, t_delta)

    animate_body(body1, body2, t_delta)


if __name__ == '__main__':
    main()