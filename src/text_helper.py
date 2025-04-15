from OpenGL.GL import *
from OpenGL.GLUT import *
import sys

class TextHelper:
    def __init__(self, active_glut_font, window_width, window_height):
        # Tenta iniciar o Glut
        self.glut_init_tried = False
        self.can_render_text = False

        self.active_glut_font = active_glut_font

        self.window_width = window_width
        self.window_height = window_height
        
        self._try_init_glut()
    
    def _try_init_glut(self):
        if self.glut_init_tried:
            return
            
        self.glut_init_tried = True
        try:
            # Tenta importar o GLUT e inicializar
            args = sys.argv if hasattr(sys, 'argv') else []
            glutInit(args)
            print("GLUT inicializado com sucesso")
            
            # Testando funções bitmap
            try:
                # Verfica se da pra chamar essa função
                if callable(glutBitmapCharacter):
                    print("glutBitmapCharacter is callable.")
                    font = self.active_glut_font
                    if font is not None:
                        self.can_render_text = True
                        # print("Renderização de texto disponível.")
                        # print("Usando a fonte GLUT:", font)
                    else:
                        print("ERRO FATAL: Fonte GLUT não disponível.")
                        sys.exit(1)
                else:
                    print("glutBitmapCharacter nao disponível.")
            except Exception as e:
                print(f"Error testing GLUT bitmap: {e}")
                print("glutBitmapCharacter nao disponível.")
                
        except Exception as e:
            print(f"Erro ao inicializar GLUT: {e}")
            return False

    # Renderiza texto na tela usando GLUT
    def render_text(self, text, x, y, font=None, color=(1.0, 1.0, 1.0)):
            
        # Define a projeção e modelo de matriz
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        try:
            import glfw # Teste: Importando o GLFW aqui
            current_context = glfw.get_current_context()
            if current_context:
                self.window_width, self.window_height = glfw.get_window_size(current_context)
        except:
            pass 
        
        glOrtho(0, self.window_width, 0, self.window_height, -1, 1)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Seta a cor do texto
        glColor3f(*color)
        
        # Verifica se da pra usar o glut pra renderizar
        if self.can_render_text:
            self._render_text_glut(text, x, y, font)
        else:
            print("Erro: Não é possível renderizar texto com GLUT.")
            sys.exit(1)

        # Renicia a matriz de projeção e modelo
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    def _render_text_glut(self, text, x, y, font=None):
        try:
            # Posição do texto recebida por parametro
            glRasterPos2f(x, y)

            # Para cada caractere no texto, renderiza
            for i in range(len(text)):
                try:
                    char = text[i]
                    if len(char) == 1:
                        # caractere padrão
                        glutBitmapCharacter(self.active_glut_font, ord(char))
                    else:
                        # caso for uma string mais comprida
                        # print(f"Erro: String muito longa para renderizar: {char}")
                        glutBitmapCharacter(self.active_glut_font, ord(char[0]))
                except Exception as e:
                    print(f"Error renderizando caractere '{char}': {e}")
                    continue
                
        except Exception as e:
            print(f"Impossível renderizar texto: {e}")
            sys.exit(1)
