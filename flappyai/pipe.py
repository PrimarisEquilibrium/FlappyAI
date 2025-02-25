import pygame
import random
from config import SCREEN_WIDTH, FLOOR_Y, SCROLL_SPEED

# A flappy bird pipe
class Pipe:
    def __init__(self, x):
        self.x = x
        self.opening = random.randint(100, int(FLOOR_Y - 100)) # The point where the pipe is open
        self.opening_size = 80
        self.pipe_speed = 250
    
    def draw(self, surface):
        top_pipe = pygame.image.load("./assets/sprites/pipe.png")
        top_pipe = pygame.transform.scale_by(top_pipe, 1.6)
        bottom_pipe = pygame.transform.rotate(top_pipe, 180)
        surface.blit(top_pipe, (self.x, self.opening + self.opening_size))
        surface.blit(bottom_pipe, (self.x, self.opening - self.opening_size - bottom_pipe.get_height()))
    
    def update(self, dt):
        self.x -= SCROLL_SPEED * dt

# Handles a collection of pipes
class PipeManager:
    def __init__(self):
        self.pipes = []
        self.timer = 0
    
    def spawn_pipe(self):
        self.pipes.append(Pipe(SCREEN_WIDTH + 50))
    
    def draw_pipes(self, surface):
        for pipe in self.pipes:
            pipe.draw(surface)
    
    def update_pipes(self, dt):
        if pygame.time.get_ticks() - self.timer > 1500:
            self.spawn_pipe()
            self.timer = pygame.time.get_ticks()
        for pipe in self.pipes:
            pipe.update(dt)