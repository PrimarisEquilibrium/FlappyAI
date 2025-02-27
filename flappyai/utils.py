import pygame

def display_text(surface, text, font_size, color, x, y, centered=False):
    """Draws text on the screen.

    Args:
        surface (pygame.Surface): The surface to draw the text on.
        text (str): The text string to draw.
        font_size (int): Font size.
        color: The color of the text, can be string, rgb tuple, pygame Color, etc.
        x (Number): x-position of the text.
        y (Number): y-position of the text.
        centered (bool, optional): If the origin point of the text box is at the center. Defaults to False.
    """
    font = pygame.font.SysFont(None, font_size)
    text = font.render(str(text), True, color)
    if centered:
        text_rect = text.get_rect(center=(x, y))
        surface.blit(text, text_rect)
    else:
        surface.blit(text, (x, y))