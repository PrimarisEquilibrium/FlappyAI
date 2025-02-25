import pygame

def display_text(surface, text, font_size, color, x, y, centered=False):
    font = pygame.font.SysFont(None, font_size)
    text = font.render(str(text), True, color)
    if centered:
        text_rect = text.get_rect(center=(x, y))
        surface.blit(text, text_rect)
    else:
        surface.blit(text, (x, y))