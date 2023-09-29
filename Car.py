import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math

from Textures import Texture
from Basura import Basura

basuras = []
distancia_evasion = 10


class Car:

    def __init__(self, posx, posz, textures):
        self.ocupado = False
        self.basura_recogida = None
        #self.velocidad = vel
        #self.basura = basura
        #self.Size = size
        self.vertexCoords = [
            1, 1, 1,   1, 1, -1,   1, -1, -1,   1, -1, 1,
            -1, 1, 1,  -1, 1, -1,  -1, -1, -1,  -1, -1, 1]

        #self.DimBoard = dim
        self.Position = (posx, 11, posz)
        self.Direction = [random.uniform(-1, 1), 0, random.uniform(-1, 1)]
        self.normalize(self.Direction)
        #self.scale(self.Direction, vel)

        self.textures = textures  # Asigna la lista de texturas

    def check_collision(self, basura):
        # Calcula las distancias en cada eje
        dx = abs(self.Position[0] - basura.Position[0])
        dy = abs(self.Position[1] - basura.Position[1])
        dz = abs(self.Position[2] - basura.Position[2])

    # Calcula las mitades de los tamaños de los objetos
        half_size_cube = self.Size/1.2
        half_size_basura = basura.Size/1.2

    # Comprueba la colisión en cada eje
        if dx <= half_size_cube + half_size_basura and \
                dy <= half_size_cube + half_size_basura and \
                dz <= half_size_cube + half_size_basura:
            return True
        else:
            return False

    def recoger_basura(self, basura_id):
        self.ocupado = True  # Marcar al robot como ocupado
        self.basura_recogida = basura_id

    def update(self, posx, posz):
        self.Position = (posx, 11, posz)

      
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
