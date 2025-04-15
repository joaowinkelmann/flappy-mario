from OpenGL.GL import *
from OpenGL.GLUT import *

class UI:
    def render(self, score, lives):
        # Renderizar pontuação e vidas
        self.render_score(score)
        self.render_lives(lives)
    
    def render_score(self, score):
        # Renderizar pontuação no canto superior
        glColor3f(1.0, 1.0, 1.0)  # Branco
        
        # Na implementação real, renderizaríamos texto
        # Por enquanto, apenas desenharemos um indicador
        glPushMatrix()
        glTranslatef(0.8, 0.9, 0)
        
        # Desenhar um pequeno quadrado para cada ponto
        for i in range(min(score, 10)):
            glBegin(GL_QUADS)
            glVertex2f(-0.01 + i*0.02, -0.01)
            glVertex2f(0.01 + i*0.02, -0.01)
            glVertex2f(0.01 + i*0.02, 0.01)
            glVertex2f(-0.01 + i*0.02, 0.01)
            glEnd()
            
        glPopMatrix()
    
    def render_lives(self, lives):
        # Renderizar vidas no canto superior esquerdo
        glColor3f(1.0, 0.0, 0.0)  # Vermelho
        
        glPushMatrix()
        glTranslatef(-0.9, 0.9, 0)
        
        # Desenhar um pequeno coração para cada vida
        for i in range(lives):
            glBegin(GL_TRIANGLES)
            # Forma simplificada de coração
            glVertex2f(0.00 + i*0.05, 0.00)
            glVertex2f(-0.02 + i*0.05, 0.02)
            glVertex2f(0.02 + i*0.05, 0.02)
            glEnd()
            
        glPopMatrix()