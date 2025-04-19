from OpenGL.GL import *
from PIL import Image
import numpy as np
import os

class TextureManager:
    def __init__(self):
        self.textures = {}
    
    def load_textures(self):     
        # Carrega o diretorio atual
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Lista de texturas existentes
        existing_textures = ["player", "pipe", "background", "extra_life", "speed_boost", "invincibility"]
        
        for name in existing_textures:
            path = os.path.join(current_dir, "assets", f"{name}.png")
            texture_id = self.load_texture_from_file(path)
            if texture_id is not None:
                self.textures[name] = texture_id
                print(f"Textura carregada com sucesso: {name}")
            else:
                print(f"Falha ao carregar textura: {path}")

    
    def load_texture_from_file(self, filename): 
        # Carrega textura de um arquivo usando PIL
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        
        # Configura parâmetros de textura
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        try:
            # Carrega a imagem e converte para RGBA
            image = Image.open(filename).convert("RGBA")
            img_data = np.array(image, dtype=np.uint8)

            
            # Enviar dados da imagem para o OpenGL
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 
                         0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
            
            return texture_id
        except Exception as e:
            print(f"Erro ao carregar textura {filename}: {e}")
            return None
    
    def bind_texture(self, name):
        # Ativar uma textura para uso
        if name in self.textures:
            glBindTexture(GL_TEXTURE_2D, self.textures[name])
            return True
        return False