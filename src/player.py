import numpy as np
from OpenGL.GL import *

class Player:
    def __init__(self, x=0.3, y=0.5, width=0.05, height=0.05, 
                 gravity=-9.8, flap_force=5.0, terminal_velocity=-10.0):
        # Posição inicial
        self.x = x  # Posição horizontal (constante)
        self.y = y  # Posição vertical (varia com a gravidade)
        
        # Física
        self.velocity = 0.0
        self.gravity = gravity
        self.flap_force = flap_force
        self.terminal_velocity = terminal_velocity
        # self.tangible = True  # se o player é tangível (verificar, talvez usar com powerup)
        
        # Tamanho do jogador (para colisões)
        self.width = width
        self.height = height
        
        # Estado
        self.alive = True
        self.speed_multiplier = 1.0
    
    def update(self, delta_time):
        # Aplicar gravidade
        self.velocity += self.gravity * delta_time
        
        # Limitar velocidade terminal (máxima queda)
        if self.velocity < self.terminal_velocity:
            self.velocity = self.terminal_velocity
            
        # Atualizar posição
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
    
    def reset_position(self):
        # Resetar posição após perder uma vida
        self.y = 0.5
        self.velocity = 0.0
    
    def render(self, renderer):
        # Chamada para renderizar o jogador
        renderer.render_player(self.x, self.y, self.width, self.height)