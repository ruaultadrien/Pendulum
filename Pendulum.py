# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 11:57:27 2016

@author: Adrien
"""


import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy.integrate as integrate





def main():
    
    
    theta0 = math.pi/2
    phi0 = 0
    init = [theta0,phi0]
    
    mass = 0.5
    radius = 0.025
    visco = 100 * 1e-3
    frot = 6*math.pi*radius*visco
    
    r = 5
    g = 9.81
    frottements = 'yes'
    param = r, g, frottements
    
    t = np.linspace(0,100,1000)
    print(t.shape[0])
    
    
    def func(y,t,param):
        theta = y[0]
        phi = y[1]
        r, g, frottements = param
        if frottements == 'yes':
            derivs = [phi, (-g/r)*math.sin(theta)-(frot/mass)*phi]
        else:
            derivs = [phi, (-g/r)*math.sin(theta)]
        
        return derivs
    
    
    sol = integrate.odeint(func, init, t, args=(param,))
    print(len(sol[:,0]))
    x = r*np.sin(sol[:,0])
    y = -r*np.cos(sol[:,0])
    
    Kinetic = 0.5*mass*(r*sol[:,1])**2
    Potential = mass*g*(r*np.sin(sol[:,0]) + r)
    Tot = Kinetic + Potential
    
    fig1 = plt.figure()
    ax = fig1.add_subplot(111)
    ax.plot(t,Kinetic,c='r')
    ax.plot(t,Potential,c='b')
    ax.plot(t,Tot,c='g')
    plt.savefig('Energy')
    
    fig2 = plt.figure()
    ax = fig2.add_subplot(111)
    line, = ax.plot([],[])

    ax.set_xlim(-6,6)
    ax.set_ylim(-6,1)
    
    
    def init():
        line.set_data([],[])
        return line,
    
    
    
    def animate(i,x,y):
        line.set_data([0,x[i]],[0,y[i]])
        return line,
        
    anim = animation.FuncAnimation(fig2,animate,init_func = init, fargs = (x,y), frames = t.shape[0], blit=True, repeat = False)
    
    anim.save('pendulum.mp4', fps=60, dpi=150, extra_args=['-vcodec', 'libx264'])
    
    

main()






