import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Basura import Basura

import random
import math
from Textures import Texture
from Car import Car
from Llanta import Llanta

screen_width = 500
screen_height = 500
FOVY = 60.0
ZNEAR = 0.01
ZFAR = 900.0
EYE_X = 300.0
EYE_Y = 200.0
EYE_Z = 300.0
CENTER_X = 0
CENTER_Y = 0
CENTER_Z = 0
UP_X = 0
UP_Y = 1
UP_Z = 0
X_MIN = -500
X_MAX = 500
Y_MIN = -500
Y_MAX = 500
Z_MIN = -500
Z_MAX = 500
DimBoard = 200

pygame.init()

Cars = []
nCars = 10

basuras = []
nbasuras = 20

textures = []





def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    glColor3f(1.0, 0.0, 0.0)  # X axis in red
    glBegin(GL_LINES)
    glVertex3f(X_MIN, 0.0, 0.0)
    glVertex3f(X_MAX, 0.0, 0.0)
    glEnd()

    glColor3f(0.0, 1.0, 0.0)  # Y axis in green
    glBegin(GL_LINES)
    glVertex3f(0.0, Y_MIN, 0.0)
    glVertex3f(0.0, Y_MAX, 0.0)
    glEnd()

    glColor3f(0.0, 0.0, 1.0)  # Z axis in blue
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, Z_MIN)
    glVertex3f(0.0, 0.0, Z_MAX)
    glEnd()

    glLineWidth(1.0)

def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: Cars")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width / screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Definir y cargar las texturas aquí
    textures.append(Texture("textura.bmp"))
    textures.append(Texture("creeper.bmp"))

    for i in range(nbasuras):
        random_x = random.uniform(-DimBoard, DimBoard)
        random_z = random.uniform(-DimBoard, DimBoard)
        basuras.append(Basura(random_x, 10, random_z, 15))

    for i in range(nCars):
        Cars.append(Car(DimBoard, 3.0, textures))  # Pasa la lista de texturas como argumento

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    glEnable(GL_TEXTURE_2D)  # Habilita la textura
    glBindTexture(GL_TEXTURE_2D, textures[0].id)  # Bind la textura cargada

    glColor(1, 1, 1)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)  # Coordenadas de textura para el vértice 1
    glVertex3d(-DimBoard, 0, -DimBoard)

    glTexCoord2f(1, 0)  # Coordenadas de textura para el vértice 2
    glVertex3d(-DimBoard, 0, DimBoard)

    glTexCoord2f(1, 1)  # Coordenadas de textura para el vértice 3
    glVertex3d(DimBoard, 0, DimBoard)

    glTexCoord2f(0, 1)  # Coordenadas de textura para el vértice 4
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()

    glDisable(GL_TEXTURE_2D)  # Deshabilita la textura

    for obj in Cars:
        glColor(1, 1, 1)
        obj.draw()
        obj.update()
        
        # Crea y dibuja las cuatro llantas debajo del carro
        front_left_wheel = Llanta(obj.Position[0] - 10, obj.Position[2] - 10)
        front_right_wheel = Llanta(obj.Position[0] - 10, obj.Position[2] + 10)
        rear_left_wheel = Llanta(obj.Position[0] + 10, obj.Position[2] - 10)
        rear_right_wheel = Llanta(obj.Position[0] + 10, obj.Position[2] + 10)

        front_left_wheel.draw()
        front_right_wheel.draw()
        rear_left_wheel.draw()
        rear_right_wheel.draw()

        # Actualiza la posición de las llantas junto con el carro
        front_left_wheel.update(obj.Position)
        front_right_wheel.update(obj.Position)
        rear_left_wheel.update(obj.Position)
        rear_right_wheel.update(obj.Position)
        
        for bs in basuras:       
            bs.draw()


def main():
    Init()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        display()

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()