import pygame
from config import FLOOR_Y


class Bird:
    """Represents a Flappy bird
    """
    bird_scale = 1.6
    bird = pygame.image.load("./assets/sprites/bird.png")
    bird = pygame.transform.scale_by(bird, bird_scale)

    def __init__(self, x, y):
        """Initialize the Bird object.

        Args:
            x (Number): Initial x-position of the bird.
            y (Number): Initial y-position of the bird.
        """
        self.x = x
        self.y = y

        self.ctr_x = self.bird.get_width() / 2
        self.ctr_y = self.bird.get_height() / 2

        self.y_velocity = 0
        self.y_acceleration = 980
        self.terminal_velocity = 600

        self.state = 2
        self.animation_timer = 0
        self.going_up = True

        self.is_alive = True
    
    def update(self, dt):
        """Updates the velocity and position of the bird.

        Args:
            dt (Number): Delta time.
        """
        # Update velocity
        self.y_velocity += self.y_acceleration * dt
        if self.y_velocity > self.terminal_velocity:
            self.y_velocity = self.terminal_velocity
            
        # Update position
        self.y += self.y_velocity * dt
    
    def has_collided(self, pipe_manager):
        """Determines if the bird has collided with a pipe.

        Args:
            pipe_manager (PipeManager): The pipe manager.

        Returns:
            bool: True if the bird has collided with a pipe; otherwise False.
        """
        if pipe_manager.collided_with_pipes(self):
            self.is_alive = False
            return True
        return False
        
    def is_out_of_bounds(self):
        """Determines if the bird is out of bounds.

        Returns:
            bool: True if the bird is out of bounds; otherwise False.
        """
        if self.y + self.ctr_y >= FLOOR_Y or self.y - self.ctr_y < 0:
            self.is_alive = False
            return True
        return False
        
    def jump(self):
        """Makes the bird "jump".
        """
        self.y_velocity = -350
    
    def get_hitbox(self):
        """Returns the current hitbox of the bird.

        Returns:
            pygame.Rect: The hitbox Rect of the bird.
        """
        return pygame.Rect(
            self.x - self.ctr_x, 
            self.y - self.ctr_y, 
            self.bird.get_width(), 
            self.bird.get_height()
        )
    
    def animate(self):
        """Animates the bird.
        """
        if pygame.time.get_ticks() - self.animation_timer < 100:
            return
        self.animation_timer = pygame.time.get_ticks()

        if self.state == 1:
            self.bird = pygame.image.load("./assets/sprites/bird-down.png")
        elif self.state == 2:
            self.bird = pygame.image.load("./assets/sprites/bird.png")
        elif self.state == 3:
            self.bird = pygame.image.load("./assets/sprites/bird-up.png")
        self.bird = pygame.transform.scale_by(self.bird, self.bird_scale)
        if self.going_up:
            self.state += 1
            if self.state == 3:
                self.going_up = False
        else:
            self.state -= 1
            if self.state == 1:
                self.going_up = True
    
    def draw(self, surface):
        """Draws the bird onto to screen.

        Args:
            surface (pygame.Surface): The surface to draw the bird on.
        """
        surface.blit(self.bird, (self.x - self.ctr_x, self.y - self.ctr_y))