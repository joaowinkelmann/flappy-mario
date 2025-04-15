import glfw
import time
from OpenGL.GL import *
import numpy as np
import random

from src.player import Player
from src.obstacles import ObstacleManager
from src.collectibles import CollectibleManager
from src.renderer import Renderer
from src.ui import UI

class Game:
    def __init__(self, window):
        self.window = window
        self.width, self.height = glfw.get_window_size(window)
        
        # Configurar callbacks de entrada
        glfw.set_key_callback(window, self.key_callback)
        
        # Estado do jogo
        self.running = True
        self.paused = False
        self.score = 0
        self.lives = 3
        
        # Inicializar componentes do jogo
        self.renderer = Renderer()
        self.player = Player()
        self.obstacle_manager = ObstacleManager()
        self.collectible_manager = CollectibleManager()
        self.ui = UI()
        
        # Configurações de tempo
        self.last_time = time.time()
        self.delta_time = 0
    
    def key_callback(self, window, key, scancode, action, mods):
        # Tratar entrada do teclado
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            self.running = False
        
        if key == glfw.KEY_SPACE and action == glfw.PRESS:
            self.player.flap()
    
    def update(self):
        # Calcular delta time
        current_time = time.time()
        self.delta_time = current_time - self.last_time
        self.last_time = current_time
        
        # Atualizar componentes do jogo
        self.player.update(self.delta_time)
        self.obstacle_manager.update(self.delta_time)
        self.collectible_manager.update(self.delta_time)
        
        # Verificar colisões
        self.check_collisions()
        
        # Aumentar pontuação se passou por obstáculo
        if self.obstacle_manager.check_passed(self.player):
            self.score += 1
    
    def check_collisions(self):
        # Verificar colisão com obstáculos
        if self.obstacle_manager.check_collision(self.player):
            self.lives -= 1
            if self.lives <= 0:
                self.game_over()
            else:
                self.reset_player()
        
        # Verificar colisão com coletáveis
        collected = self.collectible_manager.check_collection(self.player)
        for item_type in collected:
            self.apply_collectible_effect(item_type)
    
    def apply_collectible_effect(self, item_type):
        # Aplicar efeito do item coletado
        if item_type == "extra_life":
            self.lives += 1
        elif item_type == "speed_boost":
            self.player.boost_speed()
        # Outros efeitos podem ser adicionados
    
    def game_over(self):
        # Fim de jogo
        self.paused = True
        print("Game Over! Score:", self.score)
    
    def render(self):
        # Limpar tela
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Renderizar componentes
        self.renderer.render_background()
        self.obstacle_manager.render(self.renderer)
        self.collectible_manager.render(self.renderer)
        self.player.render(self.renderer)
        self.ui.render(self.score, self.lives)
        
        # Trocar buffers
        glfw.swap_buffers(self.window)
    
    def run(self):
        # Loop principal do jogo
        while self.running and not glfw.window_should_close(self.window):
            # Processar eventos
            glfw.poll_events()
            
            if not self.paused:
                self.update()
            
            self.render()