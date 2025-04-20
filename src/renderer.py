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
        
        self.aspect_ratio = 1.0  # inicialmente 1:1

        # Gerenciador de texturas
        self.texture_manager = TextureManager()
        self.texture_manager.load_textures()
    
    def update_aspect_ratio(self, width, height):
        self.aspect_ratio = width / float(height) if height != 0 else 1.0

    def render_background(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-1, 1, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_TEXTURE_2D)
        if self.texture_manager.bind_texture("background"):
            glColor4f(1.0, 1.0, 1.0, 1.0)  # Branco para manter a textura original

            # Ajusta com base no aspect ratio para cobrir toda a tela
            tex_width = 1.0
            tex_height = 1.0
            
            if self.aspect_ratio > 1.0:  # tela mais larga que alta
                # Expande horizontalmente para cobrir toda a largura
                tex_scale_x = self.aspect_ratio
                tex_scale_y = 1.0
            else:  # tela mais alta que larga
                # Expande verticalmente para cobrir toda a altura
                tex_scale_x = 1.0
                tex_scale_y = 1.0 / self.aspect_ratio
            
            # Usando coordenadas de textura ajustadas para cobrir toda a área
            glBegin(GL_QUADS)
            # Define maior área para garantir cobertura total
            left = -tex_scale_x
            right = tex_scale_x
            bottom = -tex_scale_y
            top = tex_scale_y
            
            # Ajusta coordenadas de textura para manter a parte inferior do fundo visível
            # e permitir corte na parte superior se necessário
            glTexCoord2f(0, 1); glVertex2f(left, bottom)
            glTexCoord2f(1, 1); glVertex2f(right, bottom)
            glTexCoord2f(1, 0); glVertex2f(right, top)
            glTexCoord2f(0, 0); glVertex2f(left, top)
            glEnd()


            glBegin(GL_QUADS)
            glTexCoord2f(0, 1); glVertex2f(-1, -1) 
            glTexCoord2f(1, 1); glVertex2f(1, -1)
            glTexCoord2f(1, 0); glVertex2f(1, 1)
            glTexCoord2f(0, 0); glVertex2f(-1, 1) 
            glEnd()
        else:
            # Fallback caso não consiga carregar textura
            glDisable(GL_TEXTURE_2D)

            # Céu
            if self.aspect_ratio > 1.0:
                left = -self.aspect_ratio
                right = self.aspect_ratio
                bottom = -1.0
                top = 1.0
            else:
                left = -1.0
                right = 1.0
                bottom = -1.0/self.aspect_ratio
                top = 1.0/self.aspect_ratio
                
            glColor3f(0.5, 0.7, 1.0)
            glBegin(GL_QUADS)
            glVertex2f(left, bottom)
            glVertex2f(right, bottom)
            glVertex2f(right, top)
            glVertex2f(left, top)
            glEnd()

            # Grama
            glColor3f(0.3, 0.8, 0.3)
            glBegin(GL_QUADS)
            glVertex2f(left, bottom)
            glVertex2f(right, bottom)
            glVertex2f(right, bottom + 0.2)  # altura fixa para a grama
            glVertex2f(left, bottom + 0.2)
            glEnd()

        glDisable(GL_TEXTURE_2D)

    
    def render_player(self, x, y, width, height, intangible):

         # Configurar a projeção para manter a proporção correta
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if self.aspect_ratio >= 1.0:
            # Janela mais larga que alta
            gluOrtho2D(-self.aspect_ratio, self.aspect_ratio, -1, 1)
        else:
            # Janela mais alta que larga
            gluOrtho2D(-1, 1, -1/self.aspect_ratio, 1/self.aspect_ratio)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        width = width * 5
        height = height * 5
        
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
         # Configurar a projeção para manter a proporção correta
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if self.aspect_ratio >= 1.0:
            # Janela mais larga que alta
            gluOrtho2D(-self.aspect_ratio, self.aspect_ratio, -1, 1)
        else:
            # Janela mais alta que larga
            gluOrtho2D(-1, 1, -1/self.aspect_ratio, 1/self.aspect_ratio)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

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
        if self.texture_manager.bind_texture("pipe"):
            glColor4f(1.0, 1.0, 1.0, 1.0)
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0); glVertex2f(left_top, top_pipe['bottom'])
            glTexCoord2f(1, 0); glVertex2f(right_top, top_pipe['bottom'])
            glTexCoord2f(1, 1); glVertex2f(right_top, top_pipe['top'])
            glTexCoord2f(0, 1); glVertex2f(left_top, top_pipe['top'])
            glEnd()

        # Tubo inferior (textura invertida)
        if self.texture_manager.bind_texture("pipe"):
            glColor4f(1.0, 1.0, 1.0, 1.0)
            glBegin(GL_QUADS)
            glTexCoord2f(0, 1); glVertex2f(left_bottom, bottom_pipe['bottom'])
            glTexCoord2f(1, 1); glVertex2f(right_bottom, bottom_pipe['bottom'])
            glTexCoord2f(1, 0); glVertex2f(right_bottom, bottom_pipe['top'])
            glTexCoord2f(0, 0); glVertex2f(left_bottom, bottom_pipe['top'])
            glEnd()

        glDisable(GL_TEXTURE_2D)

    
    def render_collectible(self, collectible):
         # Configurar a projeção para manter a proporção correta
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if self.aspect_ratio >= 1.0:
            # Janela mais larga que alta
            gluOrtho2D(-self.aspect_ratio, self.aspect_ratio, -1, 1)
        else:
            # Janela mais alta que larga
            gluOrtho2D(-1, 1, -1/self.aspect_ratio, 1/self.aspect_ratio)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glPushMatrix()
        glTranslatef(collectible.x, collectible.y, 0)

        # Fatores de escala
        scale_factors = {
            "extra_life": (2.5, 2.5),
            "speed_boost": (2.5, 2.5),
            "invincibility": (2.5, 2.5)
        }

        # Pega os fatores ou usa (1, 1) como padrão
        scale_x, scale_y = scale_factors.get(collectible.item_type, (1, 1))
        width = collectible.width * scale_x
        height = collectible.height * scale_y

        def render_textured_quad(texture_name):
            glEnable(GL_TEXTURE_2D)
            if self.texture_manager.bind_texture(texture_name):
                glColor4f(1.0, 1.0, 1.0, 1.0)
                glBegin(GL_QUADS)
                glTexCoord2f(0, 1); glVertex2f(-width/2, -height/2)
                glTexCoord2f(1, 1); glVertex2f(width/2, -height/2)
                glTexCoord2f(1, 0); glVertex2f(width/2, height/2)
                glTexCoord2f(0, 0); glVertex2f(-width/2, height/2)
                glEnd()
            else:
                glDisable(GL_TEXTURE_2D)
                fallback_colors = {
                    "extra_life": (1.0, 0.0, 0.0),
                    "speed_boost": (0.0, 0.0, 1.0),
                    "invincibility": (1.0, 0.5, 0.0)
                }
                glColor3f(*fallback_colors.get(collectible.item_type, (1.0, 1.0, 1.0)))
                self._draw_collectible_circle(collectible)
            glDisable(GL_TEXTURE_2D)

        if collectible.item_type == "extra_life":
            render_textured_quad("extra_life")
        elif collectible.item_type == "speed_boost":
            render_textured_quad("speed_boost")
        elif collectible.item_type == "invincibility":
            render_textured_quad("invincibility")
        else:
            glColor3f(1.0, 1.0, 1.0)
            self._draw_collectible_circle(collectible)

        glPopMatrix()

    def _draw_collectible_circle(self, collectible):
        glBegin(GL_POLYGON)
        num_segments = 16
        for i in range(num_segments):
            theta = 2.0 * np.pi * i / num_segments
            x = collectible.width / 2 * np.cos(theta)
            y = collectible.height / 2 * np.sin(theta)
            glVertex2f(x, y)
        glEnd()