import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math

from Textures import Texture

class Car:
    
    def __init__(self, dim, vel,textures):
        self.vertexCoords = [
                   1,1,1,   1,1,-1,   1,-1,-1,   1,-1,1,
                  -1,1,1,  -1,1,-1,  -1,-1,-1,  -1,-1,1  ]

        self.DimBoard = dim
        self.Position = [random.uniform(-dim, dim), 20, random.uniform(-dim, dim)]
        self.Direction = [random.uniform(-1, 1), 0, random.uniform(-1, 1)]
        self.normalize(self.Direction)
        self.scale(self.Direction, vel)
        self.textures = textures  # Asigna la lista de texturas
        
    def update(self):
        new_position = [self.Position[0] + self.Direction[0], self.Position[1], self.Position[2] + self.Direction[2]]
        
        # Verifica si la nueva posición está dentro del borde del plano
        if -self.DimBoard < new_position[0] < self.DimBoard and -self.DimBoard < new_position[2] < self.DimBoard:
            self.Position = new_position
        else:
            # El carro ha colisionado con el borde del plano, cambia de dirección en un ángulo aleatorio entre 90 y 150 grados
            angle = math.radians(random.uniform(90, 150))  # Ángulo aleatorio en radianes
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            
            # Aplica la rotación en el plano XY
            new_direction_x = self.Direction[0] * cos_a - self.Direction[2] * sin_a
            new_direction_z = self.Direction[0] * sin_a + self.Direction[2] * cos_a
            
            self.Direction = [new_direction_x, self.Direction[1], new_direction_z]

    

    def draw_colored_cube(self, x, y, z, s):
        glEnable(GL_TEXTURE_2D)  # Habilita la textura
        glBindTexture(GL_TEXTURE_2D, self.textures[1].id)  # Enlaza la textura

        glBegin(GL_QUADS)

        # Cara frontal
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x - s, y - s, z + s)

        glTexCoord2f(1.0, 0.0)
        glVertex3f(x + s, y - s, z + s)

        glTexCoord2f(1.0, 1.0)
        glVertex3f(x + s, y + s, z + s)

        glTexCoord2f(0.0, 1.0)
        glVertex3f(x - s, y + s, z + s)

        # Cara trasera
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x + s, y - s, z - s)

        glTexCoord2f(1.0, 0.0)
        glVertex3f(x - s, y - s, z - s)

        glTexCoord2f(1.0, 1.0)
        glVertex3f(x - s, y + s, z - s)

        glTexCoord2f(0.0, 1.0)
        glVertex3f(x + s, y + s, z - s)


        # Cara inferior
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x - s, y - s, z + s)

        glTexCoord2f(1.0, 0.0)
        glVertex3f(x + s, y - s, z + s)

        glTexCoord2f(1.0, 1.0)
        glVertex3f(x + s, y - s, z - s)

        glTexCoord2f(0.0, 1.0)
        glVertex3f(x - s, y - s, z - s)

        # Cara izquierda
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x - s, y - s, z + s)

        glTexCoord2f(1.0, 0.0)
        glVertex3f(x - s, y - s, z - s)

        glTexCoord2f(1.0, 1.0)
        glVertex3f(x - s, y + s, z - s)

        glTexCoord2f(0.0, 1.0)
        glVertex3f(x - s, y + s, z + s)

        # Cara derecha
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x + s, y - s, z + s)

        glTexCoord2f(1.0, 0.0)
        glVertex3f(x + s, y - s, z - s)

        glTexCoord2f(1.0, 1.0)
        glVertex3f(x + s, y + s, z - s)

        glTexCoord2f(0.0, 1.0)
        glVertex3f(x + s, y + s, z + s)

        glEnd()

        glDisable(GL_TEXTURE_2D)  # Deshabilita la textura


    def draw(self):
        glPushMatrix()
        
        # Calcula el ángulo de rotación en radianes basado en la dirección de movimiento
        angle = math.atan2(self.Direction[2], self.Direction[0])

        # Aplica la rotación alrededor del eje Y
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glRotatef(math.degrees(angle), 0, 1, 0)  # Rota alrededor del eje Y
        glScaled(20, 20, 20)
        
        self.draw_colored_cube(0, 0, 0, 0.5)
        glPopMatrix()

    def normalize(self, v):
        length = math.sqrt(v[0] ** 2 + v[2] ** 2)
        if length != 0:
            v[0] /= length
            v[2] /= length
    
    def scale(self, v, s):
        v[0] *= s
        v[2] *= s