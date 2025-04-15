from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

class Renderer:
    def __init__(self):
        # Inicializar OpenGL
        glClearColor(0.5, 0.7, 1.0, 1.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        
        # TODO
        # # Gerenciador de texturas
        # self.texture_manager = TextureManager()
        # self.texture_manager.load_textures()
    
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
    
    def render_player(self, x, y, width, height):
        # Renderizar o jogador (pássaro)
        glColor3f(1.0, 1.0, 0.0)  # Amarelo
        
        glPushMatrix()
        glTranslatef(x, y, 0)
        
        # Desenhar retângulo ou aplicar textura
        glBegin(GL_QUADS)
        glVertex2f(-width/2, -height/2)
        glVertex2f(width/2, -height/2)
        glVertex2f(width/2, height/2)
        glVertex2f(-width/2, height/2)
        glEnd()
        
        glPopMatrix()
    
    def render_obstacle(self, obstacle):
        # Renderizar um obstáculo (par de tubos)
        glColor3f(0.0, 0.8, 0.0)  # Verde
        
        bounds = obstacle.get_bounds()
        
        # Tubo superior
        top_pipe = bounds['top_pipe']
        glBegin(GL_QUADS)
        glVertex2f(top_pipe['left'], top_pipe['bottom'])
        glVertex2f(top_pipe['right'], top_pipe['bottom'])
        glVertex2f(top_pipe['right'], top_pipe['top'])
        glVertex2f(top_pipe['left'], top_pipe['top'])
        glEnd()
        
        # Tubo inferior
        bottom_pipe = bounds['bottom_pipe']
        glBegin(GL_QUADS)
        glVertex2f(bottom_pipe['left'], bottom_pipe['bottom'])
        glVertex2f(bottom_pipe['right'], bottom_pipe['bottom'])
        glVertex2f(bottom_pipe['right'], bottom_pipe['top'])
        glVertex2f(bottom_pipe['left'], bottom_pipe['top'])
        glEnd()
    
    def render_collectible(self, collectible):
        # Renderizar um item coletável
        if collectible.item_type == "extra_life":
            glColor3f(1.0, 0.0, 0.0)  # Vermelho para vida extra
        elif collectible.item_type == "speed_boost":
            glColor3f(0.0, 0.0, 1.0)  # Azul para boost de velocidade
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