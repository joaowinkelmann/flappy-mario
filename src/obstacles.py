import random
import numpy as np
from OpenGL.GL import *

class Obstacle:
    def __init__(self, x, gap_center, gap_size, obstacle_width):
        self.x = x  # Posição horizontal
        self.gap_center = gap_center  # Posição vertical do centro do gap
        self.gap_size = gap_size  # Tamanho da abertura
        self.obstacle_width = obstacle_width
        self.passed = False  # Flag para verificar se o jogador já passou
    
    def update(self, delta_time, speed):
        # Mover o obstáculo para a esquerda
        self.x -= speed * delta_time
    
    def get_bounds(self):
        # Retorna os limites dos tubos superior e inferior
        return {
            'top_pipe': {
                'left': self.x - self.obstacle_width/2,
                'right': self.x + self.obstacle_width/2,
                'top': 1.0,
                'bottom': self.gap_center + self.gap_size/2
            },
            'bottom_pipe': {
                'left': self.x - self.obstacle_width/2,
                'right': self.x + self.obstacle_width/2,
                'top': self.gap_center - self.gap_size/2,
                'bottom': -1.0
            }
        }
    
    def check_collision(self, player):
        # Verificar colisão com o jogador
        player_bounds = player.get_bounds()
        pipe_bounds = self.get_bounds()
        
        # Colisão com tubo superior
        if (player_bounds['right'] > pipe_bounds['top_pipe']['left'] and
            player_bounds['left'] < pipe_bounds['top_pipe']['right'] and
            player_bounds['top'] > pipe_bounds['top_pipe']['bottom']):
            return True
        
        # Colisão com tubo inferior
        if (player_bounds['right'] > pipe_bounds['bottom_pipe']['left'] and
            player_bounds['left'] < pipe_bounds['bottom_pipe']['right'] and
            player_bounds['bottom'] < pipe_bounds['bottom_pipe']['top']):
            return True
        
        return False
    
    def is_passed_by(self, player_x):
        # Verifica se o jogador passou pelo obstáculo
        if not self.passed and player_x > self.x:
            self.passed = True
            return True
        return False
    
    def render(self, renderer):
        # Renderizar os tubos superior e inferior
        renderer.render_obstacle(self)


class ObstacleManager:
    def __init__(self, speed=0.5, spawn_interval=2.0, gap_size=0.3, obstacle_width=0.1):
        self.obstacles = []
        self.spawn_timer = 0
        self.spawn_interval = spawn_interval  # Intervalo entre novos obstáculos
        self.speed = speed  # Velocidade base
        self.gap_size = gap_size  # Tamanho da abertura entre os tubos
        self.obstacle_width = obstacle_width  # Largura dos obstáculos
    
    def update(self, delta_time):
        # Atualizar timer para spawn de novos obstáculos
        self.spawn_timer += delta_time
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self.spawn_obstacle()
        
        # Atualizar obstáculos existentes
        for obstacle in self.obstacles[:]:
            obstacle.update(delta_time, self.speed)
            
            # Remover obstáculos que saíram da tela
            if obstacle.x < -1.5:
                self.obstacles.remove(obstacle)
    
    def spawn_obstacle(self):
        # Criar novo obstáculo
        gap_center = random.uniform(-0.3, 0.3)
        new_obstacle = Obstacle(1.2, gap_center, self.gap_size, self.obstacle_width)
        self.obstacles.append(new_obstacle)
    
    def check_collision(self, player):
        # se o player ta invencivel, ja sai
        if player.intangible:
            return
        
        # Verificar colisão com todos os obstáculos
        for obstacle in self.obstacles:
            if obstacle.check_collision(player):
                return True
        return False
    
    def check_passed(self, player):
        # Verificar se o jogador passou por algum obstáculo
        score_increased = False
        for obstacle in self.obstacles:
            if obstacle.is_passed_by(player.x):
                score_increased = True
        return score_increased
    
    def render(self, renderer):
        # Renderizar todos os obstáculos
        for obstacle in self.obstacles:
            obstacle.render(renderer)