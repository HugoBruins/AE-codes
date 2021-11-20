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
g = 9.80665

rho0 = 1.225
Pa0 = 274.94
CLmax = 1.340471

# Drag polar 
cd0 = 0.0195
k1 = -0.0212
k2 = 0.034

# Gravity parameters
mu = 398600.441*(10**9)
R = 6378136

# Turning this off illustrates that the lines continuous 
clean = True

# Empty lists plot later
Vmax = []
Vmin = []
Vmincl = []
altitudes = []

def gravity(h):
    return (mu)/((R + h)**2)

# A function to get the air density at a given altitude
def Density(h, g):
    return rho0 *((288.15 - 0.0065*h)/(288.15))**((-1*g) / (287 * -0.0065) - 1)

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
    rho = Density(h, g)
    W = m*g
    # Vmin is the intersection from the left hand side, so the initial guess is low
    vmin = Newtons_Method(P_R, rho, 7, 50, 0.0000001)
    # Vmax is the intersection from the right hand side, so the initial guess is high
    vmax = Newtons_Method(P_R, rho, 40, 50, 0.0000001)
    # Calculating vmin based on CLmax as lift being the limiting factor
    vminLift = np.sqrt((2*W)/(CLmax * S * rho))
    if not clean:
        Vmincl.append(vminLift)
        Vmax.append(vmax)
        Vmin.append(vmin)
        altitudes.append(h)
    else:
        if (vmax != None and vmin != None and vminLift != None):
            Vmax.append(vmax)
            altitudes.append(h)
            if (vminLift > vmin):
                Vmincl.append(vminLift)
                Vmin.append(None)
            else:
                Vmin.append(vmin)
                Vmincl.append(None)
    h+=1
    if (h > 10000):
        break

fig, ax = plt.subplots(figsize=(12, 6))
plt.xlim([0, 60])
plt.ylim([0, 10000])
ax.plot(Vmax, altitudes , color='blue', label='Maximum Velocity')
ax.plot(Vmin, altitudes , color='red', label='Minimum Velocity Power Limit')
ax.plot(Vmincl, altitudes , color='fuchsia', label='Minimum Velocity Stall limit')
plt.xlabel('Velocity (m/s)')
plt.ylabel('Altitude (m)')
plt.grid()
ax.legend()
