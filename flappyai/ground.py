import pygame
from config import SCREEN_WIDTH, SCROLL_SPEED, FLOOR_Y


class Ground:
    """Represents the ground of the Flappy Bird game.
    """
    ground_img = pygame.image.load("./assets/sprites/ground.png")
    ground_img = pygame.transform.scale_by(ground_img, 1.25)
    ground_width = ground_img.get_width()

    def __init__(self, x, y):
        """Initialize the Ground object

        Args:
            x (Number): The initial x-position of the ground.
            y (Number): The initial y-position of the ground.
        """
        self.x = x
        self.y = y
    
    def update(self, dt):
        """Updates the position of the ground.

        Args:
            dt (Number): Delta time.
        """
        self.x -= SCROLL_SPEED * dt

    def draw(self, surface):
        surface.blit(self.ground_img, (self.x, self.y))

class GroundManager:
    """Represents a collection of grounds and their subsequent operations.
    """
    def __init__(self):
        """Initialize the GroundManager object.
        """
        self.ground_array = []
    
    def create_ground(self):
        """Continually creates Ground objects from left-to-right until it fills the screen.
        """
        furthest_x = 0
        # Keep adding the ground image until it fills the screen
        while furthest_x < SCREEN_WIDTH + self.ground_width:
            self.ground_array.append(Ground(furthest_x, FLOOR_Y))
            furthest_x += self.ground_width
    
    def update(self, dt):
        """Updates the state of all grounds.

        Args:
            dt (Number): Delta time.
        """
        for i, ground in enumerate(self.ground_array):
            # Delete any ground images that cannot be seen on the screen anymore
            # Then add a new one behind the screen
            if ground.x + self.ground_width < 0:
                self.ground_array.append(Ground(self.ground_array[-1].x + self.ground_width, FLOOR_Y))
                del self.ground_array[i]
            ground.update(dt)
    
    def draw(self, surface):
        """Draws all the grounds onto the given surface.

        Args:
            surface (pygame.Surface): The surface to draw on.
        """
        for ground in self.ground_array:
            ground.draw(surface)