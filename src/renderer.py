from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import time

from src.texture import TextureManager

class Renderer:
    def __init__(self):
        # Inicializar OpenGL
        glClearColor(0.5, 0.7, 1.0, 1.0)  # Fundo azul celeste
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Gerenciador de texturas
        self.texture_manager = TextureManager()
        self.texture_manager.load_textures()
    
    def render_background(self):
        # Renderizar o fundo do jogo
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-1, 1, -1, 1)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Renderizar céu
        glColor3f(0.5, 0.7, 1.0)
        glBegin(GL_QUADS)
        glVertex2f(-1, -1)
        glVertex2f(1, -1)
        glVertex2f(1, 1)
        glVertex2f(-1, 1)
        glEnd()
        
        # Renderizar grama
        glColor3f(0.3, 0.8, 0.3)
        glBegin(GL_QUADS)
        glVertex2f(-1, -1)
        glVertex2f(1, -1)
        glVertex2f(1, -0.8)
        glVertex2f(-1, -0.8)
        glEnd()
    
    def render_player(self, x, y, width, height, intangible):
        width = width * 4
        height = height * 4
        
        glPushMatrix()
        glTranslatef(x, y, 0)
        
        glEnable(GL_TEXTURE_2D)
        if self.texture_manager.bind_texture("player"):
            glColor4f(1.0, 1.0, 1.0, 1.0)  # Cor branca para não alterar a textura
            glBegin(GL_QUADS)
            glTexCoord2f(0, 1); glVertex2f(-width/2, -height/2)
            glTexCoord2f(1, 1); glVertex2f(width/2, -height/2)
            glTexCoord2f(1, 0); glVertex2f(width/2, height/2)
            glTexCoord2f(0, 0); glVertex2f(-width/2, height/2)
            glEnd()
        else:
            # Fallback caso não consiga carregar textura
            glDisable(GL_TEXTURE_2D)
            glColor3f(1.0, 1.0, 0.0)
            glBegin(GL_QUADS)
            glVertex2f(-width/2, -height/2)
            glVertex2f(width/2, -height/2)
            glVertex2f(width/2, height/2)
            glVertex2f(-width/2, height/2)
            glEnd()
        
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

    
    def render_obstacle(self, obstacle):
        bounds = obstacle.get_bounds()
        
        expansion = 4.5  # fator multiplicador
        center_top = (bounds['top_pipe']['left'] + bounds['top_pipe']['right']) / 2
        width_top = (bounds['top_pipe']['right'] - bounds['top_pipe']['left']) * expansion
        left_top = center_top - width_top / 2
        right_top = center_top + width_top / 2

        center_bottom = (bounds['bottom_pipe']['left'] + bounds['bottom_pipe']['right']) / 2
        width_bottom = width_top 
        left_bottom = center_bottom - width_bottom / 2
        right_bottom = center_bottom + width_bottom / 2

        top_pipe = bounds['top_pipe']
        bottom_pipe = bounds['bottom_pipe']

        glEnable(GL_TEXTURE_2D)
        
        # Tubo superior (textura normal)
        if self.texture_manager.bind_texture("cano"):
            glColor4f(1.0, 1.0, 1.0, 1.0)
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0); glVertex2f(left_top, top_pipe['bottom'])
            glTexCoord2f(1, 0); glVertex2f(right_top, top_pipe['bottom'])
            glTexCoord2f(1, 1); glVertex2f(right_top, top_pipe['top'])
            glTexCoord2f(0, 1); glVertex2f(left_top, top_pipe['top'])
            glEnd()

        # Tubo inferior (textura invertida)
        if self.texture_manager.bind_texture("cano"):
            glColor4f(1.0, 1.0, 1.0, 1.0)
            glBegin(GL_QUADS)
            glTexCoord2f(0, 1); glVertex2f(left_bottom, bottom_pipe['bottom'])
            glTexCoord2f(1, 1); glVertex2f(right_bottom, bottom_pipe['bottom'])
            glTexCoord2f(1, 0); glVertex2f(right_bottom, bottom_pipe['top'])
            glTexCoord2f(0, 0); glVertex2f(left_bottom, bottom_pipe['top'])
            glEnd()

        glDisable(GL_TEXTURE_2D)

    
    def render_collectible(self, collectible):
        # Renderizar um item coletável
        if collectible.item_type == "extra_life":
            glColor3f(1.0, 0.0, 0.0)  # Vermelho para vida extra
        elif collectible.item_type == "speed_boost":
            glColor3f(0.0, 0.0, 1.0)  # Azul para boost de velocidade
        elif collectible.item_type == "invincibility":
            glColor3f(1.0, 0.5, 0.0) # Laranja para invencibilidade
        else:
            glColor3f(1.0, 1.0, 1.0)  # Branco para outros itens
        
        glPushMatrix()
        glTranslatef(collectible.x, collectible.y, 0)
        
        # Desenhar círculo (aproximado por polígono)
        glBegin(GL_POLYGON)
        num_segments = 16
        for i in range(num_segments):
            theta = 2.0 * 3.1415926 * i / num_segments
            x = collectible.width/2 * np.cos(theta)
            y = collectible.height/2 * np.sin(theta)
            glVertex2f(x, y)
        glEnd()
        
        glPopMatrix()