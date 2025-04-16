import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from src.game import Game

# Constatntes e Configurações do Jogo

# Configurações de janela
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Jogo Flappy Bird"

# Configurações de física
GRAVITY = -9.8
FLAP_FORCE = 3.0
TERMINAL_VELOCITY = -10.0 # cap de velocidade de quedad

# Configs do jogo
OBSTACLE_SPEED = 0.5
OBSTACLE_SPAWN_INTERVAL = 2.0
OBSTACLE_GAP_SIZE = 0.6 # Tamanho do espaço vertical entre os canos
OBSTACLE_WIDTH = 0.1  # Largura dos canos
COLLECTIBLE_SPAWN_INTERVAL = 5.0  # Tempo entre cada tentativa de spawn de coletável
COLLECTIBLE_SPEED = 0.5 
INITIAL_LIVES = 5

# Configurações do jogador
PLAYER_SIZE = 0.05  # Para calcular os "bounds"/limites do jogador
PLAYER_X_POS = 0.3  # Posição horizontal do jogador (constante)
PLAYER_START_Y = 0.5  # Altura do início do jogador

# COnfigurações visuais
BACKGROUND_COLOR = (0.5, 0.7, 1.0, 1.0)
TITLE_BACKGROUND_COLOR = (0.1, 0.1, 0.2, 1.0) 
BIRD_COLOR = (1.0, 1.0, 0.0)
OBSTACLE_COLOR = (0.0, 0.8, 0.0)
EXTRA_LIFE_COLOR = (1.0, 0.0, 0.0)
SPEED_BOOST_COLOR = (0.0, 0.0, 1.0)
GLUT_ACTIVE_FONT = GLUT_BITMAP_HELVETICA_18  # Fonte a ser usada para o texto

def main():
    # Tenta iniciar o GLFW
    if not glfw.init():
        print("Erro ao inicializar o GLFW")
        return

    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, None, None)
    if not window:
        glfw.terminate()
        print("Falhou ao criar a janela")
        return

    glfw.make_context_current(window)

    # Criar instância do jogo
    game = Game(window=window,
                game_font=GLUT_ACTIVE_FONT,
                gravity=GRAVITY,
                flap_force=FLAP_FORCE, 
                terminal_velocity=TERMINAL_VELOCITY,
                obstacle_speed=OBSTACLE_SPEED,
                obstacle_spawn_interval=OBSTACLE_SPAWN_INTERVAL,
                obstacle_gap_size=OBSTACLE_GAP_SIZE,
                obstacle_width=OBSTACLE_WIDTH,
                collectible_spawn_interval=COLLECTIBLE_SPAWN_INTERVAL,
                collectible_speed=COLLECTIBLE_SPEED,
                initial_lives=INITIAL_LIVES,
                player_size=PLAYER_SIZE,
                player_x_pos=PLAYER_X_POS,
                player_start_y=PLAYER_START_Y,
                )

    # Loop principal
    game.run()

    # Limpar recursos
    glfw.terminate()

if __name__ == "__main__":
    main()