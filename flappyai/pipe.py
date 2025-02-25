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
        self.pipe_img = pygame.image.load("./assets/sprites/pipe.png")

    def draw(self, surface):
        top_pipe = pygame.transform.scale_by(self.pipe_img, 1.6)
        bottom_pipe = pygame.transform.rotate(top_pipe, 180)
        surface.blit(top_pipe, (self.x, self.opening + self.opening_size))
        surface.blit(bottom_pipe, (self.x, self.opening - self.opening_size - bottom_pipe.get_height()))
    
    # Checks if the bird has collided with the pipe
    def is_game_over(self, bird_hitbox_rect):
        return (pygame.Rect.colliderect(self.top_pipe_hitbox, bird_hitbox_rect)
                or pygame.Rect.colliderect(self.bottom_pipe_hitbox, bird_hitbox_rect))

    def has_passed_pipe(self, bird_hitbox_rect):
        return pygame.Rect.colliderect(self.opening_hitbox , bird_hitbox_rect)

    def update(self, dt):
        self.x -= SCROLL_SPEED * dt

        # Initialize/Update hitbox
        self.top_pipe_hitbox = pygame.Rect(
            self.x, 
            self.opening + self.opening_size, 
            self.pipe_img.get_width(), 
            self.pipe_img.get_height()
        )
        self.bottom_pipe_hitbox = pygame.Rect(
            self.x, 
            self.opening - self.opening_size - self.pipe_img.get_height(), 
            self.pipe_img.get_width(), 
            self.pipe_img.get_height()
        )
        self.opening_hitbox = pygame.Rect(
            self.x + self.pipe_img.get_width(), 
            self.opening - self.opening_size, 
            10, 
            self.opening_size * 2
        )

# Handles a collection of pipes
class PipeManager:
    def __init__(self):
        self.pipes = []
        self.latest_pipe = None
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
    
    def is_game_over(self, bird):
        for pipe in self.pipes:
            if pipe.is_game_over(bird):
                return True
        return False

    def has_passed_pipe(self, bird_hitbox_rect):
        for pipe in self.pipes:
            # Only count the pipe being passed one time
            if pipe.has_passed_pipe(bird_hitbox_rect) and pipe is not self.latest_pipe:
                self.latest_pipe = pipe
                return True
        return False
            