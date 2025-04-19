import glfw
import time
from OpenGL.GL import *

from src.player import Player
from src.obstacles import ObstacleManager
from src.collectibles import CollectibleManager
from src.renderer import Renderer
from src.ui import UI
from src.view import View

# Estados do jogo
TITLE = 0
PLAYING = 1
GAME_OVER = 2
DIFF_SELECT = 3 # TODO: Implementar
CONTINUE_SCREEN = 4

class Game:
    def __init__(self, window, game_font, gravity=-9.8, flap_force=5.0, terminal_velocity=-10.0,
                obstacle_speed=0.5, obstacle_spawn_interval=2.0, obstacle_gap_size=0.3, obstacle_width=0.1,
                collectible_spawn_interval=5.0, collectible_speed=0.5, initial_lives=3, player_size=0.05,
                player_x_pos=0.3, player_start_y=0.5):
        
        self.debug = False
        self.window = window
        self.width, self.height = glfw.get_window_size(window)

        # Configurar callbacks de entrada
        glfw.set_key_callback(window, self.key_callback)

        glfw.set_framebuffer_size_callback(window, self.framebuffer_size_callback)

        # Insatnciando o estado do jogo inicial
        self.state = TITLE
        self.score = 0
        self.lives = initial_lives

        # Guarda as configs do jogo, para que podemos mudar depois
        self.config = {
            'gravity': gravity,
            'flap_force': flap_force,
            'terminal_velocity': terminal_velocity,
            'obstacle_speed': obstacle_speed,
            'collectible_speed': collectible_speed,
            'obstacle_spawn_interval': obstacle_spawn_interval,
            'obstacle_gap_size': obstacle_gap_size,
            'obstacle_width': obstacle_width,
            'collectible_spawn_interval': collectible_spawn_interval,
            'player_size': player_size,
            'player_x_pos': player_x_pos,
            'player_start_y': player_start_y,
            'initial_lives': initial_lives
        }

        # Inicializar componentes do jogo
        self.renderer = Renderer()
        
        # Instancia o jogador
        self.player = Player(
            x=player_x_pos,
            y=player_start_y,
            width=player_size,
            height=player_size,
            gravity=gravity,
            flap_force=flap_force,
            terminal_velocity=terminal_velocity
        )
        
        # Inicialia o gerenciador de obstáculos e coletáveis
        self.obstacle_manager = ObstacleManager(
            speed=self.config['obstacle_speed'],
            spawn_interval=self.config['obstacle_spawn_interval'],
            gap_size=self.config['obstacle_gap_size'],
            obstacle_width=self.config['obstacle_width']
        )
        
        self.collectible_manager = CollectibleManager(
            speed=self.config['collectible_speed'],
            spawn_interval=self.config['collectible_spawn_interval']
        )
        # referncia o gerenciador de canos no gerenciador de coletáveis para fazer check de colisão
        self.collectible_manager.set_obstacle_manager(self.obstacle_manager)
        
        self.ui = UI(game_font, self.width, self.height)
        self.view = View(game_font, self.width, self.height)

        # Configurações de tempo
        self.last_time = time.time()
        self.delta_time = 0

    def key_callback(self, window, key, scancode, action, mods):
        # Tratar entrada do teclado baseado no estado do jogo
        if action == glfw.PRESS:
            if key == glfw.KEY_F3: # Modo debug
                # faz o toggle
                self.debug = not self.debug

            if key == glfw.KEY_ESCAPE:
                if self.state == CONTINUE_SCREEN:
                    # se ta no continue, game over
                    self.game_over()
                else:
                    self.running = False # sai do jogo

            if self.state == TITLE:
                if key == glfw.KEY_SPACE:
                    self.start_game()
            elif self.state == PLAYING:
                if key == glfw.KEY_SPACE:
                    self.player.flap()
            elif self.state == CONTINUE_SCREEN:
                if key == glfw.KEY_SPACE:
                    self.continue_game()
            elif self.state == GAME_OVER:
                if key == glfw.KEY_R:
                    self.restart_game()

    # inicia o jogo
    def start_game(self):
        self.state = PLAYING
        # self.score = 0
        # self.lives = 3
        # self.player.reset_position()
        # self.obstacle_manager = ObstacleManager()
        # self.collectible_manager = CollectibleManager()
        self.last_time = time.time()

    def restart_game(self):
        self.score = 0
        self.lives = self.config['initial_lives']
        self.player.reset_position()
        self.player.alive = True
        self.obstacle_manager = ObstacleManager(
            speed=self.config['obstacle_speed'],
            spawn_interval=self.config['obstacle_spawn_interval'],
            gap_size=self.config['obstacle_gap_size'],
            obstacle_width=self.config['obstacle_width']
        )
        self.collectible_manager = CollectibleManager(
            speed=self.config['collectible_speed'],
            spawn_interval=self.config['collectible_spawn_interval']
        )
        # fix: seta o gerenciador de obstáculos no reset tbm
        self.collectible_manager.set_obstacle_manager(self.obstacle_manager)
        self.state = PLAYING
        self.last_time = time.time() # Reinicia o timer do jogo

    # Loop principal do jogo que roda a cada frame
    def update(self):
        # Calcular delta time
        current_time = time.time()
        self.delta_time = current_time - self.last_time
        self.last_time = current_time

        # Faz o check somente se o jogador está jogando
        if self.state == PLAYING:
            self.player.update(self.delta_time)
            
            # se ta com speed boost, atualiza a velocidade dos obstáculos e coletáveis
            if self.player.speed_boost_active:
                effective_speed = self.config['obstacle_speed'] * self.player.speed_multiplier
                effective_collectible_speed = self.config['collectible_speed'] * self.player.speed_multiplier
            else:
                effective_speed = self.config['obstacle_speed']
                effective_collectible_speed = self.config['collectible_speed']
            
            # atualiza a velocidade dos obstáculos e coletáveis
            self.obstacle_manager.speed = effective_speed
            self.collectible_manager.speed = effective_collectible_speed

            self.obstacle_manager.update(self.delta_time)
            self.collectible_manager.update(self.delta_time)

            # Verificar colisões
            self.check_collisions()

            # Aumentar pontuação se passou por obstáculo
            if self.obstacle_manager.check_passed(self.player):
                self.score += 1

            # Se bateu no canto da tela, perde uma vida
            if self.player.y <= -1.0 + self.player.height / 2:
                 self.handle_death()


    def check_collisions(self):
        # Verificar colisão com obstáculos

        # se o player ta intangível, ja sai
        if self.player.intangible:
            return

        if self.obstacle_manager.check_collision(self.player):
            self.handle_death()
            return

        # Verificar colisão com coletáveis
        collected = self.collectible_manager.check_collection(self.player)
        for item_type in collected:
            self.apply_collectible_effect(item_type)


    # Cuida dos eventos após a morte do jogador
    def handle_death(self):
        self.lives -= 1
        
        # Pausa o jogo e mostra a tela de continue
        if self.lives <= 0:
            self.game_over()
        else:
            # chama a tela de continue
            self.state = CONTINUE_SCREEN
            # para o passarinho
            self.player.velocity = 0
            # fix: zera o boost do player
            self.player.speed_multiplier = 1.0

    def apply_collectible_effect(self, item_type):
        # Aplicar efeito do item coletado
        if item_type == "extra_life":
            self.lives += 1
        elif item_type == "speed_boost":
            self.player.boost_speed(1.5, 5.0) # Aumenta a velocidade por 5 segundos
        elif item_type == "invincibility":
            # seta com timer pra voltar a ser tangível
            self.player.activate_intangibility(5.0)
        # Outros efeitos podem ser adicionados


    def reset_player_position(self):
        # Resetar posição do jogador após perder uma vida (sem game over)
        self.player.reset_position()
        # Verificar: talvez deixar o player invencível


    def game_over(self):
        self.state = GAME_OVER
        self.player.alive = False
        print(f"Game Over! Score: {self.score}")


    def continue_game(self):
        # continua o jogo depois de perder uma das vidas
        # reseta a posição e da uma invencibilidade
        self.reset_player_position()
        self.player.activate_intangibility(duration=2.0)
        self.state = PLAYING
        self.last_time = time.time()

    # Renderiza os elementos do jogo, baseando-se nos estados
    def render(self):
        if self.state == TITLE:
             self.view.render_title_screen()
        else:
             # Limpa a tela e reinicia a cor de fundo
             glClearColor(0.5, 0.7, 1.0, 1.0)
             glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
             self.renderer.render_background()

             # Renderiza os objetos do jogo
             self.obstacle_manager.render(self.renderer)
             self.collectible_manager.render(self.renderer)
             if self.player.alive or self.state == GAME_OVER:
                  self.player.render(self.renderer)

             # HUD só aparece com o jogo rodando
             if self.state == PLAYING:
                  
                  if self.debug:
                    player_bounds = self.player.get_bounds()
                    self.ui.render_debug(f"Bounds: {player_bounds}")
                    self.ui.render_debug(f"Velocity: {self.player.velocity:.2f}")
                    self.ui.render_debug(f"Pos: {self.player.x:.2f}, {self.player.y:.2f}")
                    fps = 1.0 / self.delta_time if self.delta_time > 0 else 0
                    self.ui.render_debug(f"FPS: {fps:.2f}")

                    if self.player.intangible:
                        self.ui.render_debug(f"Intangível: {self.player.intangible_timer:.1f}s")
                    if self.player.speed_boost_active:
                        self.ui.render_debug(f"Boost: {self.player.speed_boost_timer:.1f}s")

                  self.ui.render(self.score, self.lives)
             elif self.state == GAME_OVER:
                  # Puxa a tela de game over
                  self.view.render_game_over_screen(self.score)
             elif self.state == CONTINUE_SCREEN:
                  # Puxa a tela de continue
                  self.view.render_continue_screen(self.lives)

        # Trocar buffers
        glfw.swap_buffers(self.window)

    def run(self):
        # Configura o viewport inicial
        glViewport(0, 0, self.width, self.height)

        # Loop principal do jogo
        self.running = True
        while self.running and not glfw.window_should_close(self.window):
            # Processar eventos
            glfw.poll_events()

            # Se não ta na tela de título, chama o loop de lógica a rodar a cada frame
            if self.state != TITLE:
                self.update()

            self.render()

    def framebuffer_size_callback(self, window, width, height):
        # Atualiza o viewport para cobrir toda a nova janela
        glViewport(0, 0, width, height)

        # Atualiza as dimensões armazenadas da janela
        self.width, self.height = width, height

        # Atualiza o aspect ratio no renderer
        if hasattr(self, 'renderer'):
            self.renderer.update_aspect_ratio(width, height)