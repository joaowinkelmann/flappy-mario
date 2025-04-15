import numpy as np
from OpenGL.GL import *

class Player:
    def __init__(self):
        self.x = 0.3  # Posição horizontal
        self.y = 0.5  # Posição vertical
        
        # Física
        self.velocity = 0.0
        self.gravity = -9.8
        self.flap_force = 5.0
        
        # Tamanho do jogador (para colisões)
        self.width = 0.05
        self.height = 0.05
        
        # Estado
        self.alive = True
        self.speed_multiplier = 1.0
    
    def update(self, delta_time):
        # Aplicar gravidade
        self.velocity += self.gravity * delta_time
        self.y += self.velocity * delta_time
        
        # Limitar posição vertical (não sair da tela)
        if self.y < -1.0 + self.height:
            self.y = -1.0 + self.height
            self.velocity = 0
        elif self.y > 1.0 - self.height:
            self.y = 1.0 - self.height
            self.velocity = 0
    
    def flap(self):
        # Salto quando pressiona espaço
        self.velocity = self.flap_force
    
    def get_bounds(self):
        # Retorna os limites para verificação de colisão
        return {
            'left': self.x - self.width/2,
            'right': self.x + self.width/2,
            'top': self.y + self.height/2,
            'bottom': self.y - self.height/2
        }
    
    def boost_speed(self):
        # Ativa power-up de velocidade
        self.speed_multiplier = 1.5
        # (Na implementação real, adicionaríamos um timer)
    
    def render(self, renderer):
        # Chamada para renderizar o jogador
        renderer.render_player(self.x, self.y, self.width, self.height)