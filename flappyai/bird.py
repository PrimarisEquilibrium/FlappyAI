import pygame
from config import SCREEN_HEIGHT

# Represents the "flappy" bird
class Bird:
    def __init__(self, x, y, bird_scale):
        self.x = x
        self.y = y

        self.bird = pygame.image.load("./assets/sprites/bird.png")
        self.bird = pygame.transform.scale_by(self.bird, bird_scale)
        self.ctr_x = self.bird.get_width() / 2
        self.ctr_y = self.bird.get_height() / 2

        self.y_velocity = 0
        self.y_acceleration = 0.5
        self.terminal_velocity = 8
    
    def update(self, event_list, dt):
        for event in event_list:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.y_velocity = -10
                
        # Update velocity
        self.y_velocity += self.y_acceleration
        if self.y_velocity > self.terminal_velocity:
            self.y_velocity = self.terminal_velocity
            
        # Update position
        self.y += self.y_velocity

        # !! Death triggers (boundaries for now)
        if self.y + self.ctr_y >= SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.ctr_y
        if self.y - self.ctr_y < 0:
            self.y = self.ctr_y
            self.y_velocity = 0
    
    def draw(self, surface):
        surface.blit(self.bird, (self.x - self.ctr_x, self.y - self.ctr_y))