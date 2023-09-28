import requests
from Llanta import Llanta
from Car import Car
from Textures import Texture
import math
import random
from Basura import Basura
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from pygame.locals import *
import pygame


URL_BASE = "http://localhost:5100"
r = requests.post(URL_BASE + "/games", allow_redirects=False)

LOCATION = r.headers["Location"]
print(LOCATION)
lista = r.json()

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

DimBoard = 210

factor = 20

pygame.init()
'''
Cars = []
nCars = 5

basuras = []

basuras_recogidas = []

nbasuras = 25

'''
textures = []

# Variables para el movimiento del plano
plane_x = 0
plane_z = 0
plane_speed = 5  # Ajusta la velocidad de movimiento


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


bots = {}
basuras = {}
# print(lista)


def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: Cars")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width / screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X,
              CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Definir y cargar las texturas
    textures.append(Texture("textura.bmp"))
    textures.append(Texture("creeper.bmp"))
    textures.append(Texture("texturabasura.bmp"))

    print("Lista:0", lista[0])

    # print("\nLista:1", lista[1])

    for agent in lista[0]:
        car = Car(agent["x"]*factor-DimBoard,
                  agent["z"]*factor-DimBoard, textures)
        bots[agent["id"]] = car

    for agent in lista[1]:
        basura = Basura(agent["x"]*factor-DimBoard,
                        agent["z"]*factor-DimBoard, textures)
        basuras[agent["id"]] = basura


def display():
    response = requests.get(URL_BASE + LOCATION)
    lista = response.json()
    print(lista[0])
    print(URL_BASE+LOCATION)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    glTranslatef(plane_x, 0, plane_z)
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

    for bs in basuras.values():
        glColor(1, 1, 1)
        bs.draw()

    for obj in bots.values():
        glColor(1, 1, 1)
        obj.draw()

    for agent in lista[0]:
        bots[agent["id"]].update(
            agent["x"]*factor-DimBoard, agent["z"]*factor-DimBoard)
        print(agent["x"],agent["z"])
    for agent in lista[1]:
        basuras[agent["id"]].update(
            agent["x"]*factor-DimBoard, agent["z"]*factor-DimBoard)

    '''# Crea y dibuja las cuatro llantas debajo del carro
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
        rear_right_wheel.update(obj.Position)'''


'''
        for basura in basuras:
            if (abs(obj.Position[0]) < 1 or abs(obj.Position[2]) < 1) and basura.id == obj.basura_recogida and obj.check_collision(basura):
                basuras.remove(basura)
                obj.ocupado = False  # El robot ya no está ocupado

            if not obj.ocupado and obj.check_collision(basura) and basura.id not in basuras_recogidas:
                new_basura_y = obj.Position[1] + obj.Size / 2 + basura.Size / 2
                basura.Position = [obj.Position[0],
                                   new_basura_y, obj.Position[2]]
                # Marcar al robot como ocupado y pasar el ID de la basura
                obj.recoger_basura(basura.id)
                basuras_recogidas.append(basura.id)

            if basura.id == obj.basura_recogida and obj.check_collision(basura):
                new_basura_y = obj.Position[1] + obj.Size / 2 + basura.Size / 2
                basura.Position = [obj.Position[0],
                                   new_basura_y, obj.Position[2]]
'''


def main():
    global EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z
    # Inicializamos el ángulo de rotación a 45 grados en radianes
    angle = math.radians(45)

    radius = 400  # Radio para la rotación

    Init()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    EYE_Y += plane_speed
                    CENTER_Y += plane_speed
                elif event.key == pygame.K_s:
                    EYE_Y -= plane_speed
                    CENTER_Y -= plane_speed
                elif event.key == pygame.K_a:
                    angle += plane_speed / 10  # Aumentar el ángulo de rotación
                elif event.key == pygame.K_d:
                    angle -= plane_speed / 40  # Disminuir el ángulo de rotación

        # Calculamos las nuevas coordenadas de la cámara
        EYE_X = CENTER_X + radius * math.cos(angle)
        EYE_Z = CENTER_Z + radius * math.sin(angle)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X,
                  CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)

        display()

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()


if __name__ == "__main__":
    main()
