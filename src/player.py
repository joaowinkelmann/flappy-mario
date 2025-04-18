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
        self.intangible = False
        self.speed_boost_active = False
    
    def update(self, delta_time):
        # Aplicar gravidade
        self.velocity += self.gravity * delta_time
        
        # Limitar velocidade terminal (máxima queda)
        if self.velocity < self.terminal_velocity:
            self.velocity = self.terminal_velocity
            
        # Atualizar posição
        self.y += self.velocity * delta_time
        
        # corrigindo lógica de colisão, considerando a altura do personagem
        if self.y < -1.0 + self.height/2:
            self.y = -1.0 + self.height/2
            self.velocity = 0
        elif self.y > 1.0 - self.height/2:
            self.y = 1.0 - self.height/2
            self.velocity = 0
            
        # Atualiza os timers de power-ups
        self.update_timers(delta_time)
    
    def update_timers(self, delta_time):
        # check do timer de intangibilidade
        if self.intangible:
            self.intangible_timer -= delta_time
            if self.intangible_timer <= 0:
                self.intangible = False
                self.intangible_timer = 0
        
        # check do timer de velocidade
        if self.speed_boost_active:
            self.speed_boost_timer -= delta_time
            if self.speed_boost_timer <= 0:
                self.speed_boost_active = False
                self.speed_multiplier = 1.0
                self.speed_boost_timer = 0
    
    def activate_intangibility(self, duration=5.0):
        self.intangible = True
        self.intangible_timer = duration
    
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
    
    def boost_speed(self, multiplier, duration=5.0):
        # Ativa power-up de velocidade
        self.speed_boost_active = True
        # self.speed_multiplier = multiplier
        # EXPERIMENTAL: se ja ta ativo, aumenta ainda mais a velocidade
        self.speed_multiplier *= multiplier
        self.speed_boost_timer = duration
    
    def reset_position(self):
        # Resetar posição após perder uma vida
        self.y = 0.5
        self.velocity = 0.0
    
    def render(self, renderer):
        # Chamada para renderizar o jogador
        renderer.render_player(self.x, self.y, self.width, self.height, self.intangible)