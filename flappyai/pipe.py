import pygame
import random
from config import SCREEN_WIDTH, FLOOR_Y, SCROLL_SPEED

class Pipe:
    """Represents a Flappy Bird Pipe.
    """
    pipe_img = pygame.image.load("./assets/sprites/pipe.png")

    def __init__(self, x):
        """Initialize the Pipe object.

        Args:
            x (int): The initial x-position of the pipe.
        """
        self.x = x
        self.opening = random.randint(100, int(FLOOR_Y - 100)) # The point where the pipe is open
        self.opening_size = 80
        self.pipe_speed = 250

    def draw(self, surface):
        """Draws the Pipe object onto the given pygame surface.

        Args:
            surface (pygame.Surface): The pygame surface to draw on.
        """
        top_pipe = pygame.transform.scale_by(self.pipe_img, 1.6)
        bottom_pipe = pygame.transform.rotate(top_pipe, 180)
        surface.blit(top_pipe, (self.x, self.opening + self.opening_size))
        surface.blit(bottom_pipe, (self.x, self.opening - self.opening_size - bottom_pipe.get_height()))

    def pipe_hitbox(self, pipe_y, hitbox_rect):
        """Returns true if a pipe collides with a hitbox Rect.

        Args:
            pipe_y (Number): The y-position of the pipe.
            hitbox_rect (pygame.Rect): The hitbox Rect.

        Returns:
            bool: True if the hitbox Rect collides with the pipe; otherwise False.
        """
        return pygame.Rect.colliderect(
            pygame.Rect(
                self.x, 
                pipe_y, 
                self.pipe_img.get_width(), 
                self.pipe_img.get_height()
            ), 
            hitbox_rect
        )
    
    def is_game_over(self, bird_hitbox_rect):
        """Returns True if the bird has collided with a pipe.

        Args:
            bird_hitbox_rect (pygame.Rect): The hitbox Rect of the bird.

        Returns:
            bool: True if the bird has collided with a pipe; otherwise False.
        """
        
        return (self.pipe_hitbox(self.opening + self.opening_size, bird_hitbox_rect) or 
                self.pipe_hitbox(self.opening - self.opening_size - self.pipe_img.get_height(), bird_hitbox_rect))

    def has_passed_pipe(self, bird_hitbox_rect):
        """Returns True if the bird passes through a pipe.

        Args:
            bird_hitbox_rect (pygame.Rect): The hitbox Rect of the bird.

        Returns:
            bool: True if the bird has passed through a pipe; otherwise False.
        """

        return pygame.Rect.colliderect(
            pygame.Rect( # The pipe opening hitbox
                self.x + self.pipe_img.get_width(), 
                self.opening - self.opening_size, 
                10, 
                self.opening_size * 2
            ), 
            bird_hitbox_rect
        )

    def update(self, dt):
        """Updates the state of the Pipe.

        Args:
            dt (Number): Delta time.
        """
        self.x -= SCROLL_SPEED * dt


# Handles a collection of pipes
class PipeManager:
    def __init__(self):
        self.pipes = []
        self.latest_pased_pipe = None
        self.timer = 0
    
    def spawn_pipe(self):
        self.pipes.append(Pipe(SCREEN_WIDTH + 50))
    
    def get_closest_pipe(self, bird_x):
        for pipe in self.pipes:
            # Only returns pipes in front of the bird
            if pipe.x > bird_x:
                return pipe
    
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
            if pipe.has_passed_pipe(bird_hitbox_rect) and pipe is not self.latest_pased_pipe:
                self.latest_pased_pipe = pipe
                return True
        return False
            