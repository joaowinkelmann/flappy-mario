from src.text_helper import TextHelper

class UI:
    def __init__(self, game_font, width, height):
        # Instanciar o helper de texto
        self.text_helper = TextHelper(game_font, width, height)
        self.current_debug_height = 0
        self.debug_line_height = 20
        self.width = width
        self.height = height

    def render(self, score, lives):
        # a cada frame, reseta a altura do texto do debug
        self.reset_debug_height()
        
        # atualiza as dimensões da janela caso tenha mudado
        self.width = self.text_helper.window_width
        self.height = self.text_helper.window_height
        
        # Renderizar pontuação e vidas
        self.render_score(score)
        self.render_lives(lives)

    def render_score(self, score):
        # Renderizar pontuação no canto superior direito
        x = int(self.width * 0.80)
        y = int(self.height * 0.90)
        self.text_helper.render_text(f"Score: {score}", x, y, color=(1.0, 1.0, 1.0))

    def render_lives(self, lives):
        # Renderizar vidas no canto superior esquerdo
        x = int(self.width * 0.10)
        y = int(self.height * 0.90) 
        self.text_helper.render_text(f"Lives: {lives}", x, y, color=(1.0, 0.0, 0.0)) # Red lives text

    # Reseta a altura do texto de debug para o próximo frame
    def reset_debug_height(self):
        self.current_debug_height = 0

    # Ativa com o F3
    def render_debug(self, debug_info):
        base_y = int(self.height * 0.02)
        
        # Renderiza o texto baseado na altura atual
        self.text_helper.render_text(
            debug_info, 
            int(self.width * 0.02),
            base_y + self.current_debug_height,
            color=(1.0, 1.0, 1.0)
        )
        
        # incrementa para a próxima linha
        self.current_debug_height += self.debug_line_height