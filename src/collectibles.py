import random
import numpy as np

class Collectible:
    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.width = 0.05
        self.height = 0.05
        self.item_type = item_type  # "extra_life", "speed_boost", etc.
        self.collected = False
    
    def update(self, delta_time, speed):
        # Mover para a esquerda
        self.x -= speed * delta_time
    
    def get_bounds(self):
        # Retorna os limites para verificação de colisão
        return {
            'left': self.x - self.width/2,
            'right': self.x + self.width/2,
            'top': self.y + self.height/2,
            'bottom': self.y - self.height/2
        }
    
    def check_collision(self, player):
        # Verificar colisão com o jogador
        if self.collected:
            return False
            
        player_bounds = player.get_bounds()
        item_bounds = self.get_bounds()
        
        if (player_bounds['right'] > item_bounds['left'] and
            player_bounds['left'] < item_bounds['right'] and
            player_bounds['top'] > item_bounds['bottom'] and
            player_bounds['bottom'] < item_bounds['top']):
            self.collected = True
            return True
        
        return False
    
    def render(self, renderer):
        # Renderizar o item se não foi coletado
        if not self.collected:
            renderer.render_collectible(self)


class CollectibleManager:
    def __init__(self):
        self.collectibles = []
        self.spawn_timer = 0
        self.spawn_interval = 5.0  # Intervalo entre novos itens
        self.speed = 0.5
    
    def update(self, delta_time):
        # Atualizar timer para spawn de novos itens
        self.spawn_timer += delta_time
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self.spawn_collectible()
        
        # Atualizar itens existentes
        for item in self.collectibles[:]:
            item.update(delta_time, self.speed)
            
            # Remover itens que saíram da tela ou foram coletados
            if item.x < -1.5 or item.collected:
                self.collectibles.remove(item)
    
    def spawn_collectible(self):
        # Chance de 50% de spawnar um item
        if random.random() < 0.5:
            return
            
        # Criar novo item aleatório
        x = 1.2
        y = random.uniform(-0.8, 0.8)
        
        # Selecionar tipo aleatório
        item_types = ["extra_life", "speed_boost"]
        item_type = random.choice(item_types)
        
        new_item = Collectible(x, y, item_type)
        self.collectibles.append(new_item)
    
    def check_collection(self, player):
        # Verificar colisão com todos os itens
        collected_items = []
        for item in self.collectibles:
            if item.check_collision(player):
                collected_items.append(item.item_type)
        return collected_items
    
    def render(self, renderer):
        # Renderizar todos os itens
        for item in self.collectibles:
            item.render(renderer)