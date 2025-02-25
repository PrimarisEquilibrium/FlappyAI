import pygame
import random
from config import SCREEN_HEIGHT, SCREEN_WIDTH

# A flappy bird pipe
class Pipe:
    def __init__(self, x):
        self.x = x
        self.opening = random.randint(100, int(SCREEN_HEIGHT - 100)) # The point where the pipe is open
        self.opening_size = 90
    
    def draw(self, surface):
        top_pipe = pygame.image.load("./assets/sprites/pipe.png")
        top_pipe = pygame.transform.scale_by(top_pipe, 1.5)
        bottom_pipe = pygame.transform.rotate(top_pipe, 180)
        surface.blit(top_pipe, (self.x, self.opening + self.opening_size))
        surface.blit(bottom_pipe, (self.x, self.opening - self.opening_size - bottom_pipe.get_height()))
    
    def update(self):
        self.x -= 2

# Handles a collection of pipes
class PipeManager:
    def __init__(self):
        self.pipes = []
    
    def spawn_pipe(self):
        self.pipes.append(Pipe(SCREEN_WIDTH + 50))
    
    def draw_pipes(self, surface):
        for pipe in self.pipes:
            pipe.draw(surface)
    
    def update_pipes(self):
        for pipe in self.pipes:
            pipe.update()