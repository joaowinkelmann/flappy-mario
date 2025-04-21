import random
import numpy as np

class Collectible:
    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.width = 0.05
        self.height = 0.05
        self.item_type = item_type
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
    def __init__(self, speed=0.5, spawn_interval=5.0):
        self.collectibles = []
        self.spawn_timer = 0
        self.spawn_interval = spawn_interval # Intervalo entre novos itens
        self.speed = speed # Velocidade dos itens (geralmente igual à dos obstáculos)
        self.obstacle_manager = None # check de colisão
        self.player = None # Passando o player pra atualizar as chances de spawn de item
        self.coins_collected = 0 # Contador de moedas coletadas

    def set_obstacle_manager(self, obstacle_manager):
        self.obstacle_manager = obstacle_manager
        
    def set_player(self, player):
        self.player = player
    
    def update(self, delta_time):
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

    def is_position_valid(self, x, y, width, height):
            if self.obstacle_manager is None:
                return True
        
            for obstacle in self.obstacle_manager.obstacles:
                bounds = obstacle.get_bounds()

                # Se o item está horizontalmente sobre o obstáculo
                if bounds['bottom_pipe']['left'] < x < bounds['bottom_pipe']['right']:
                    # O Y precisa estar DENTRO do GAP.
                    gap_top = bounds['top_pipe']['bottom']
                    gap_bottom = bounds['bottom_pipe']['top']
                    if not (gap_bottom + height/2 <= y <= gap_top - height/2):
                        return False
                        
            return True

    
    def spawn_collectible(self):
        # Default: 50% de chance de spawn
        spawn_chance = 0.5
        item_types = ["extra_life", "speed_boost", "invincibility", "coin"]

        # Se o jogador estiver com speed boost, aumenta a chance de spawn
        if self.player and getattr(self.player, "speed_boost_active", False):
            spawn_chance = 0.9 # 90% de chance de spawn
            # desses 90%, 70% de chance de ser speed boost
            if random.random() < 0.7:
                forced_type = "speed_boost"
            else:
                forced_type = random.choice(item_types)
        else:
            forced_type = random.choice(item_types)

        if random.random() > spawn_chance:
            return

        pos_x = 1.2
        item_width = 0.05
        item_height = 0.05
        pos_y = random.uniform(-0.8, 0.8)

        if self.is_position_valid(pos_x, pos_y, item_width, item_height):
            new_item = Collectible(pos_x, pos_y, forced_type)
            self.collectibles.append(new_item)
            return
    
    def check_collection(self, player):
        # Verificar colisão com todos os itens
        collected_items = []
        for item in self.collectibles:
            if item.check_collision(player):
                if item.item_type == "coin":
                    self.coins_collected += 1
                collected_items.append(item.item_type)
        return collected_items
    
    def render(self, renderer):
        # Renderizar todos os itens
        for item in self.collectibles:
            item.render(renderer)