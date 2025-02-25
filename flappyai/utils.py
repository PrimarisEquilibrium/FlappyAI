import pygame

def display_text(surface, text, font_size, color, x, y, centered=False):
    font = pygame.font.SysFont(None, font_size)
    text = font.render(str(text), True, color)
    if centered:
        text_rect = text.get_rect(center=(x, y))
        surface.blit(text, text_rect)
    else:
        surface.blit(text, (x, y))

class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, surface, outline=None):
        if outline:
            pygame.draw.rect(surface, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
            
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            font = pygame.font.SysFont(None, 60)
            text = font.render(self.text, 1, (0, 0, 0))
            surface.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x, y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False