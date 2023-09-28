from OpenGL.GL import *

class Incinerator:
    def __init__(self, x, z,size):
        self.Position = (x,6, z)
        self.Size = size

    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glColor3f(0.0, 0.0, 0.0)  # Color negro para la basura

        half_size = self.Size / 2.0

        glBegin(GL_QUADS)
        
        # Cara frontal
        glVertex3f(-half_size, -half_size, 0.0)
        glVertex3f(half_size, -half_size, 0.0)
        glVertex3f(half_size, half_size, 0.0)
        glVertex3f(-half_size, half_size, 0.0)

        # Cara trasera
        glVertex3f(-half_size, half_size, -self.Size)
        glVertex3f(half_size, half_size, -self.Size)
        glVertex3f(half_size, -half_size, -self.Size)
        glVertex3f(-half_size, -half_size, -self.Size)

        # Cara lateral izquierda
        glVertex3f(-half_size, -half_size, 0.0)
        glVertex3f(-half_size, half_size, 0.0)
        glVertex3f(-half_size, half_size, -self.Size)
        glVertex3f(-half_size, -half_size, -self.Size)

        # Cara lateral derecha
        glVertex3f(half_size, -half_size, 0.0)
        glVertex3f(half_size, half_size, 0.0)
        glVertex3f(half_size, half_size, -self.Size)
        glVertex3f(half_size, -half_size, -self.Size)

        # Cara superior
        glVertex3f(-half_size, half_size, 0.0)
        glVertex3f(half_size, half_size, 0.0)
        glVertex3f(half_size, half_size, -self.Size)
        glVertex3f(-half_size, half_size, -self.Size)

        # Cara inferior
        glVertex3f(-half_size, -half_size, 0.0)
        glVertex3f(half_size, -half_size, 0.0)
        glVertex3f(half_size, -half_size, -self.Size)
        glVertex3f(-half_size, -half_size, -self.Size)
        
        glEnd()
        
        glPopMatrix()
        
    