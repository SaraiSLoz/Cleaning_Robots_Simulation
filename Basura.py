from OpenGL.GL import *

class Basura:
    def __init__(basura, posx, posz,textures):
        basura.Position = (posx, 6, posz)
        #basura.Size = size
        basura.id = id
        basura.textures = textures  # Asigna la lista de texturas
        

    def draw_textured_trash(basura,x,y,z,s):
        glEnable(GL_TEXTURE_2D)  # Habilita la textura
        glBindTexture(GL_TEXTURE_2D, basura.textures[2].id)

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

        # Cara superior
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x - s, y + s, z + s)

        glTexCoord2f(1.0, 0.0)
        glVertex3f(x + s, y + s, z + s)

        glTexCoord2f(1.0, 1.0)
        glVertex3f(x + s, y + s, z - s)

        glTexCoord2f(0.0, 1.0)
        glVertex3f(x - s, y + s, z - s)

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

    def update(self, posx, posz):
        self.Position = (posx, 6,posz)

    def draw(basura):
        glPushMatrix()
        glTranslatef(basura.Position[0], basura.Position[1], basura.Position[2])
        glScaled(20, 20, 20)
        basura.draw_textured_trash(0, 0, 0, 0.4)
        glPopMatrix()
        
    