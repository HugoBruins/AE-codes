# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 11:38:52 2021

@author: Hugo Bruins
"""
import numpy as np
import matplotlib.pyplot as plt

# Plane parameters
m = 12
S = 0.45

rho0 = 0.01456190842
Pa0 = 274.94
CLmax = 1.340471

# Drag polar 
cd0 = 0.0195
k1 = -0.0212
k2 = 0.034

# Gravity parameters
mu = 4.2828372 * (10**(13))
R = 3389500

# Clean the envelope?
clean = True
# Empty lists plot later
Vmax = []
Vmin = []
Vmincl = []
altitudes = []

def gravity(h):
    return (mu)/((R + h)**2)

def Pressure(h):
    return 699*np.exp(-0.00009 * h)

def Temperature(h):
    return 249.75 - 0.00222 * h

# A function to get the air density at a given altitude
def Density(h):
    p = Pressure(h)
    t = Temperature(h)
    rho = p / (192.1 * t)
    return rho

# A function to calculate the required power
def P_R(V, rho):
    CL = (2*W)/(V**2*S*rho) 
    Pa = rho/rho0 * Pa0
    return ((cd0 + k1*CL + k2*CL**2)*0.5*rho*V**3*S - Pa)

def f1der(f, x, h, density):
    return (f(x+h, density) - f(x, density)) / h

def Newtons_Method(f1, density, guess, iterations, h):
    for i in range(iterations):
        prevguess = guess
        guess = guess - (f1(guess, density))/(f1der(f1, guess, h,density))
        try: 
            if (round(prevguess, 13) == round(guess, 13)):
                return guess
                break
        except:
                break
    return None

h = 0
while (True):
    # Calculating gravity
    g = gravity(h)
    # Calculating the air density, and minimum maximum velocities
    rho = Density(h)
    W = m*g
    # Vmin is the intersection from the left hand side, so the initial guess is low
    vmin = Newtons_Method(P_R, rho, 7, 50, 0.0000001)
    # Vmax is the intersection from the right hand side, so the initial guess is high
    vmax = Newtons_Method(P_R, rho, 200, 50, 0.0000001)
    # Calculating vmin based on CLmax as lift being the limiting factor
    vminLift = np.sqrt((2*W)/(CLmax * S * rho))
    # Adding to the lists for plotting
    if not clean:
        Vmincl.append(vminLift)
        Vmax.append(vmax)
        Vmin.append(vmin)
        altitudes.append(h)
    else:
        if (vmax != None and vmin != None):
            Vmax.append(vmax)
            altitudes.append(h)
            if (vminLift > vmin):
                Vmincl.append(vminLift)
                Vmin.append(None)
            else:
                Vmin.append(vmin)
                Vmincl.append(None)
    
    h += 1
    if (h > 5000):
        break

fig, ax = plt.subplots(figsize=(12, 6))
plt.xlim([0, 200])
plt.ylim([0, 5000])
ax.plot(Vmax, altitudes , color='blue', label='Maximum Velocity')
ax.plot(Vmin, altitudes , color='red', label='Minimum Velocity Power Limit')
ax.plot(Vmincl, altitudes , color='fuchsia', label='Minimum Velocity Stall limit')
plt.xlabel('Velocity (m/s)')
plt.ylabel('Altitude (m)')
plt.grid()
ax.legend()
