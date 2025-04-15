from OpenGL.GL import *
from src.text_helper import TextHelper

class View:
    def __init__(self, game_font, width, height):
        self.text_helper = TextHelper(game_font, width, height)
        self.width = width
        self.height = height

    def render_title_screen(self):
        glClearColor(0.1, 0.1, 0.2, 1.0)  # Deixa um pouco mais escuro
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Define a projeção e a matriz de modelo para renderizar o texto
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1, 1, -1, 1, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        title_x = int(self.width * 0.5 - 150)
        title_y = int(self.height * 0.66)
        
        instruction_x = int(self.width * 0.5 - 125)
        instruction_y = int(self.height * 0.5)
        
        self.text_helper.render_text("Flappy Bird OpenGL", title_x, title_y, color=(1.0, 1.0, 0.0))
        self.text_helper.render_text("Press SPACE to Start", instruction_x, instruction_y, color=(1.0, 1.0, 1.0))

    def render_game_over_screen(self, score):
        # Se a tela foi redimensionada, atualiza as dimensões
        self.width = self.text_helper.window_width
        self.height = self.text_helper.window_height
    
        # Define a projeção e a matriz de modelo para renderizar o texto
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1, 1, -1, 1, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glColor4f(0.0, 0.0, 0.0, 0.5) # Deixa um pouco mais escuro
        glBegin(GL_QUADS)
        glVertex2f(-1, -1)
        glVertex2f(1, -1)
        glVertex2f(1, 1)
        glVertex2f(-1, 1)
        glEnd()
        glColor4f(1.0, 1.0, 1.0, 1.0) # Reseta a cor a ser usada

        # Calcula posições relativas para o texto
        game_over_x = int(self.width * 0.5 - 60)
        game_over_y = int(self.height * 0.7)
        
        score_x = int(self.width * 0.5 - 40)
        score_y = int(self.height * 0.6)
        
        restart_x = int(self.width * 0.5 - 80)
        restart_y = int(self.height * 0.5)
        
        quit_x = int(self.width * 0.5 - 70)
        quit_y = int(self.height * 0.4)

        # Renderiza o texto de Game Over e as instruções
        self.text_helper.render_text("Game Over!", game_over_x, game_over_y, color=(1.0, 0.0, 0.0))
        self.text_helper.render_text(f"Score: {score}", score_x, score_y, color=(1.0, 1.0, 1.0))
        self.text_helper.render_text("Press R to Restart", restart_x, restart_y, color=(1.0, 1.0, 1.0))
        self.text_helper.render_text("Press ESC to Quit", quit_x, quit_y, color=(1.0, 1.0, 1.0))