import pygame
import random
from config import SCREEN_WIDTH, FLOOR_Y, SCROLL_SPEED

class Pipe:
    """Represents a Flappy Bird Pipe.
    """
    pipe_img = pygame.image.load("./assets/sprites/pipe.png")
    bottom_pipe = pygame.transform.scale_by(pipe_img, 1.6)
    top_pipe = pygame.transform.rotate(bottom_pipe, 180)

    def __init__(self, x):
        """Initialize the Pipe object.

        Args:
            x (int): The initial x-position of the pipe.
        """
        self.x = x
        self.opening = random.randint(150, int(FLOOR_Y - 150)) # The point where the pipe is open
        self.opening_size = 85
        self.pipe_speed = 250
        self.bottom_pipe_y = self.opening + self.opening_size
        self.top_pipe_y = self.opening - self.opening_size - self.top_pipe.get_height()

    def draw(self, surface):
        """Draws the Pipe object onto the given pygame surface.

        Args:
            surface (pygame.Surface): The pygame surface to draw on.
        """
        surface.blit(self.bottom_pipe, (self.x, self.bottom_pipe_y))
        surface.blit(self.top_pipe, (self.x, self.top_pipe_y))

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
    
    def collided_with_pipe(self, bird):
        """Returns True if the bird has collided with a pipe.

        Args:
            bird (Bird): The bird object.

        Returns:
            bool: True if the bird has collided with a pipe; otherwise False.
        """
        
        return (self.pipe_hitbox(self.opening + self.opening_size, bird.get_hitbox()) or 
                self.pipe_hitbox(self.opening - self.opening_size - self.pipe_img.get_height(), bird.get_hitbox()))

    def has_passed_pipe(self, bird):
        """Returns True if the bird passes through a pipe.

        Args:
            bird (Bird): The bird object.

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
            bird.get_hitbox()
        )

    def update(self, dt):
        """Updates the state of the Pipe.

        Args:
            dt (Number): Delta time.
        """
        self.x -= SCROLL_SPEED * dt
        self.bottom_pipe_y = self.opening + self.opening_size
        self.top_pipe_y = self.opening - self.opening_size - self.top_pipe.get_height()


class PipeManager:
    """Represents a collection of pipes and their subsequent operations.
    """

    def __init__(self):
        """Initialize the PipeManager object.
        """
        self.pipes = []
        self.latest_pased_pipe = None
        self.timer = 0
    
    def spawn_pipe(self):
        """Spawns a pipe to the right beyond the rendered screen.
        """
        self.pipes.append(Pipe(SCREEN_WIDTH + 50))
    
    def get_closest_pipe(self, bird_x):
        """Returns the pipe that is closest to the bird, but not behind it.

        Args:
            bird_x (Number): The x-position of the bird.

        Returns:
            Pipe|None: The pipe closest to the bird; if a pipe isn't initialized yet, None.
        """
        for pipe in self.pipes:
            # Only returns pipes in front of the bird
            if pipe.x > bird_x:
                return pipe
    
    def draw_pipes(self, surface):
        """Draws all the stored pipes.

        Args:
            surface (pygame.Surface): The pygame surface to draw the pipes on.
        """
        for pipe in self.pipes:
            pipe.draw(surface)
    
    def update_pipes(self, dt):
        """Updates all the position and handles generation of new pipes.

        Args:
            dt (Number): Delta time.
        """
        if pygame.time.get_ticks() - self.timer > 1500:
            self.spawn_pipe()
            self.timer = pygame.time.get_ticks()
        for pipe in self.pipes:
            pipe.update(dt)
    
    def collided_with_pipes(self, bird_hitbox_rect):
        """Returns True if any pipes collided_with_pipe method is also True.

        Args:
            bird_hitbox_rect (pygame.Rect): The hitbox Rect of the bird.

        Returns:
            bool: True if the bird has collided with any pipe; otherwise False.
        """
        return any([pipe.collided_with_pipe(bird_hitbox_rect) for pipe in self.pipes])

    def has_passed_pipe(self, bird):
        """Returns True if the bird collides with opening.

        Args:
            bird (Bird): The bird object.

        Returns:
            bool: True if the bird collides with the opening hitbox; otherwise False. 
        """
        for pipe in self.pipes:
            # Only count the pipe being passed one time
            if pipe.has_passed_pipe(bird) and pipe is not self.latest_pased_pipe:
                self.latest_pased_pipe = pipe
                return True
        return False
            