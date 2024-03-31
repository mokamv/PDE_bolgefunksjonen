import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

c = 1.0  # Bølgefart
L = 2.5  # Lengde på akse
dempningsfaktor = 0.1 # Dempningsfaktor
dx = 0.1  # Steglengde
dt = 0.01  # Tidssteg

start_x = 0 # Startposisjon x
start_y = 0 # Startposisjon y

x = np.arange(-L/2, L/2, dx)
y = np.arange(-L/2, L/2, dx)
X, Y = np.meshgrid(x, y) #Matrisekoordinater

u = np.zeros_like(X) # u (Lager en nullmatrise med samme form som X)
u_t = np.zeros_like(X) # tidsderiverte av u

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d') 
ax.set_xlim(-L/2, L/2) #Setter grenser for x-aksen
ax.set_ylim(-L/2, L/2) #Setter grenser for y-aksen
ax.set_zlim(0, 0.3) #Setter grenser for z-aksen

surface = [ax.plot_surface(X, Y, u, cmap='coolwarm')] #plotter overflaten

def update_wave(i):
    global u, u_t

    u_new = u + dt*u_t
    u_t_new = u_t + dt*c**2*(np.roll(u, -1, axis=0) + np.roll(u, 1, axis=0) + np.roll(u, -1, axis=1) + np.roll(u, 1, axis=1) - 4*u)/dx**2 - dempningsfaktor*u_t
    # psudo: u_t_new = u_t + dt*u_tt - dempningsfaktor*u_t
    # psudo: u_tt = c**2 * laplace(u)
    # psudo: u_t_new = u_t + dt*(c**2 * laplace(u)) - dempningsfaktor*u_t)
    u, u_t = u_new, u_t_new

    surface[0].remove() #Fjerner den eksisterende overflaten
    surface[0] = ax.plot_surface(X, Y, u, cmap='coolwarm') #Plotter overflaten på nytt

def on_click(event):
    x = int((start_x + L/2)/dx)
    y = int((start_y + L/2)/dx)

    # Initialverdier
    u[y, x] = 1.0
    u_t[y, x] = 0.0


fig.canvas.mpl_connect('button_press_event', on_click)
ani = FuncAnimation(fig, update_wave, frames=100, interval=100) #Oppdaterer bølgen 100 ganger med 100ms mellomrom

plt.show()