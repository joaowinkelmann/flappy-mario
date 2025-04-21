import ctypes # da stdlib do python
from OpenGL.GL import *
from OpenGL.GLUT import *
from src.text_helper import TextHelper

class View:
    def __init__(self, game_font, width, height):
        self.text_helper = TextHelper(game_font, width, height)
        self.width = width
        self.height = height

    # atualiza as dimensões da tela, caso tenha mudado, pegando do TextHelper
    def update_dimensions(self):
        self.width = self.text_helper.window_width
        self.height = self.text_helper.window_height

    # Calcula a posição X para centralizar o texto na tela
    def center_x(self, text):
        font = self.text_helper.active_glut_font
        if not text or not font:
            # Se o texto for vazio ou a fonte não estiver definida, retorna o centro (para outros elementos não texto)
            return int(self.width * 0.5)
            
        # coifica para bytes pra não dar erro de codificação ao calcular
        encoded_text = text.encode('utf-8')
        
        # Cria um buffer de string a partir dos bytes codificados
        c_text = ctypes.create_string_buffer(encoded_text)
        
        # Converte o buffer para o tipo esperado pela função glutBitmapLength
        ptr = ctypes.cast(c_text, ctypes.POINTER(ctypes.c_ubyte))
        
        # Obtém a largura do texto em pixels pegando a fonte GLUT ativa
        text_width = glutBitmapLength(font, ptr)
        
        # Calcula a posição X inicial para centralizar o texto
        return int(self.width * 0.5 - text_width / 2)

    def render_title_screen(self):
        self.update_dimensions() # Garante que as dimensões estão atualizadas
        glClearColor(0.1, 0.1, 0.2, 1.0)  # Fundo azul escuro para o título
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Define a projeção e a matriz de modelo para renderizar o texto
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # Usar glOrtho padrão para elementos do jogo, se houver
        glOrtho(-1, 1, -1, 1, -1, 1) 
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Desenha um ícone de pássaro amarelo (usando coordenadas normalizadas)
        # Essas coordenadas são relativas ao centro (0,0)
        bird_x_center = 0.0
        bird_y_center = 0.5 # Posiciona o pássaro um pouco acima do centro
        bird_scale = 0.1    # Tamanho do pássaro
        glColor3f(1.0, 1.0, 0.0) # Cor amarela
        glBegin(GL_TRIANGLES)
        glVertex2f(bird_x_center, bird_y_center + bird_scale) # Topo
        glVertex2f(bird_x_center - bird_scale * 0.5, bird_y_center - bird_scale * 0.5) # Base esquerda
        glVertex2f(bird_x_center + bird_scale * 0.5, bird_y_center - bird_scale * 0.5) # Base direita
        glEnd()

        # Define os textos
        title_text = "Flappy Bird OpenGL"
        instruction_text = "Press SPACE to Start"

        # Calcula as posições Y
        title_y = int(self.height * 0.66) # Posição Y do título
        instruction_y = int(self.height * 0.5) # Posição Y da instrução

        # Calcula as posições X centralizadas
        title_x = self.center_x(title_text)
        instruction_x = self.center_x(instruction_text)

        # Renderiza os textos usando TextHelper
        self.text_helper.render_text(title_text, title_x, title_y, (1.0, 1.0, 0.0))  # Título amarelo
        self.text_helper.render_text(instruction_text, instruction_x, instruction_y, (1.0, 1.0, 1.0))  # Instrução branca

    def render_game_over_screen(self, score, max_speed):
        """Renderiza a tela de game over com sobreposição e texto."""
        self.update_dimensions() # Garante que as dimensões estão atualizadas

        # Define a projeção e a matriz de modelo para renderizar o texto
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1, 1, -1, 1, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Desenha uma sobreposição preta semi-transparente para escurecer o fundo
        glColor4f(0.0, 0.0, 0.0, 0.5)  # Preto com 50% de transparência
        glBegin(GL_QUADS)
        glVertex2f(-1, -1)
        glVertex2f(1, -1)
        glVertex2f(1, 1)
        glVertex2f(-1, 1)
        glEnd()
        glColor4f(1.0, 1.0, 1.0, 1.0)  # Reseta a cor para branco opaco para o texto

        # Define os textos
        game_over_text = "Game Over!"
        score_text = f"Score: {score}"
        max_speed_text = f"Max Speed: {max_speed:.1f}"
        restart_text = "Press R to Restart"
        quit_text = "Press ESC to Quit"

        # Calcula as posições Y
        game_over_y = int(self.height * 0.7)
        score_y = int(self.height * 0.6)
        max_speed_y = int(self.height * 0.5)
        restart_y = int(self.height * 0.4)
        quit_y = int(self.height * 0.3)

        # Calcula as posições X centralizadas para cada texto
        game_over_x = self.center_x(game_over_text)
        score_x = self.center_x(score_text)
        max_speed_x = self.center_x(max_speed_text)
        restart_x = self.center_x(restart_text)
        quit_x = self.center_x(quit_text)

        # Renderiza os textos usando TextHelper
        self.text_helper.render_text(game_over_text, game_over_x, game_over_y, (1.0, 0.0, 0.0)) # Vermelho
        self.text_helper.render_text(score_text, score_x, score_y, (1.0, 1.0, 1.0)) # Branco
        self.text_helper.render_text(max_speed_text, max_speed_x, max_speed_y, (1.0, 1.0, 1.0)) # Branco
        self.text_helper.render_text(restart_text, restart_x, restart_y, (1.0, 1.0, 1.0)) # Branco
        self.text_helper.render_text(quit_text, quit_x, quit_y, (1.0, 1.0, 1.0)) # Branco

    def render_continue_screen(self, lives):
        """Renderiza a tela de pausa para continuar após perder uma vida."""
        self.update_dimensions() # Garante que as dimensões estão atualizadas

        # Define a projeção e a matriz de modelo para renderizar o texto
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1, 1, -1, 1, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Desenha uma sobreposição amarela semi-transparente para indicar estado temporário
        glColor4f(1.0, 1.0, 0.0, 0.2)  # Amarelo com 20% de transparência
        glBegin(GL_QUADS)
        glVertex2f(-1, -1)
        glVertex2f(1, -1)
        glVertex2f(1, 1)
        glVertex2f(-1, 1)
        glEnd()
        glColor4f(1.0, 1.0, 1.0, 1.0)  # Reseta a cor para branco opaco para o texto

        # Define os textos
        lives_text = f"Lives remaining: {lives}"
        options_text = "Press SPACE to continue or ESC to quit"

        # Calcula as posições Y
        lives_y = int(self.height * 0.55) # Um pouco acima do centro
        options_y = int(self.height * 0.45) # Um pouco abaixo do centro

        # Calcula as posições X centralizadas
        lives_x = self.center_x(lives_text)
        options_x = self.center_x(options_text)

        # Renderiza os textos usando TextHelper
        self.text_helper.render_text(lives_text, lives_x, lives_y, (1.0, 1.0, 1.0)) # Branco
        self.text_helper.render_text(options_text, options_x, options_y, (1.0, 1.0, 1.0)) # Branco