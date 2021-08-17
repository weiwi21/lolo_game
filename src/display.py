import pygame

DIMENSION = 60


class Display():
    # create base variables and sets the font
    def __init__(self):
        self.screen = None
        self.board = None
        self.X_DIMENSION = None
        self.Y_DIMENSION = None
        self.font = pygame.font.Font('font/joystix_monospace.ttf', 68)

    # gets board from game booard class
    def set_board(self, board):
        self.board = board

    # creates screen from scale
    def set_screen(self, scale):
        x = int(scale[0]) * DIMENSION
        y = int(scale[1]) * DIMENSION

        self.X_DIMENSION = x
        self.Y_DIMENSION = y
        screen = pygame.display.set_mode((x, y))
        self.screen = screen

    # draws grid board based off scale and dimension size
    def draw_board(self):
        y = 0
        for row in self.board:
            x = 0
            for cell in row:
                self.screen.blit(cell.get_image(), pygame.Rect(x * DIMENSION, y * DIMENSION, DIMENSION, DIMENSION))
                x += 1
            y += 1
        pygame.display.update()

    # draws inputed tex
    def draw_text(self, text):
        text = self.font.render(text, False, (0, 0, 255), None)
        text_rect = text.get_rect()
        text_rect.center = (660 // 2, 660 // 2)
        self.screen.blit(text, text_rect)
        pygame.display.update()
