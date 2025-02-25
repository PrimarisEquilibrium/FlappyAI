import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

ground_img = pygame.image.load("./assets/sprites/ground.png")
ground_img = pygame.transform.scale_by(ground_img, 1.25)
ground_width = ground_img.get_width()

class Ground:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def update(self, dt):
        self.x -= 150 * dt

    def draw(self, surface):
        surface.blit(ground_img, (self.x, self.y))

class GroundManager:
    def __init__(self):
        self.ground_array = []
    
    def create_ground(self):
        furthest_x = 0
        # Keep adding the ground image until it fills the screen
        while furthest_x < SCREEN_WIDTH + ground_width:
            self.ground_array.append(Ground(furthest_x, SCREEN_HEIGHT - 100))
            furthest_x += ground_width
    
    def update(self, dt):
        for i, ground in enumerate(self.ground_array):
            # Delete any ground images that cannot be seen on the screen anymore
            # Then add a new one behind the screen
            if ground.x + ground_width < 0:
                self.ground_array.append(Ground(self.ground_array[-1].x + ground_width, SCREEN_HEIGHT - 100))
                del self.ground_array[i]
            ground.update(dt)
    
    def draw(self, surface):
        for ground in self.ground_array:
            ground.draw(surface)