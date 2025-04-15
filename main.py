import glfw
from src.game import Game

def main():
    # Inicializar GLFW
    if not glfw.init():
        return
    
    # Criar janela e contexto OpenGL
    window = glfw.create_window(800, 600, "Jogo Flappy Bird", None, None)
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    
    # Criar instância do jogo
    game = Game(window)
    
    # Loop principal
    game.run()
    
    # Limpar recursos
    glfw.terminate()

if __name__ == "__main__":
    main()