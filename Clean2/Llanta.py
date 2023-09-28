
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math


class Llanta:
    def __init__(llanta, x, z):
        llanta.x = x
        llanta.z = z

    def draw(llanta):
        glPushMatrix()
        glColor3f(0.0, 0.0, 0.0)  # Color de la llanta 
        glTranslatef(llanta.x, 10, llanta.z)  # Posición de la llanta debajo del carro

        num_segments = 100  # Número de segmentos para aproximar el círculo
        radius = 5  # Radio de la llanta

        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0, 0, 0)  # Centro de la llanta
        for i in range(num_segments + 1):
            theta = 2.0 * math.pi * i / num_segments
            x = radius * math.cos(theta)
            z = radius * math.sin(theta)
            glVertex3f(x, 0, z)
        glEnd()

        glPopMatrix()

    def update(llanta, car_position):
        # Actualiza la posición de la llanta junto con el carro
        
        llanta.x = car_position[0]
        llanta.z = car_position[2]
