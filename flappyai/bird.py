import pygame
from config import FLOOR_Y

# Represents the "flappy" bird
class Bird:
    bird_scale = 1.8
    bird = pygame.image.load("./assets/sprites/bird.png")
    bird = pygame.transform.scale_by(bird, bird_scale)

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.ctr_x = self.bird.get_width() / 2
        self.ctr_y = self.bird.get_height() / 2

        self.y_velocity = 0
        self.y_acceleration = 9.8
        self.terminal_velocity = 600

        self.state = 2
        self.animation_timer = 0
        self.going_up = True

        self.is_alive = True
    
    # Returns false if game over (bird hits the ceiling or ground)
    def update(self, dt, pipe_manager):    
        # Update velocity
        self.y_velocity += self.y_acceleration
        if self.y_velocity > self.terminal_velocity:
            self.y_velocity = self.terminal_velocity
            
        # Update position
        self.y += self.y_velocity * dt

        if pipe_manager.collided_with_pipes(self):
            self.is_alive = False
        if self.y + self.ctr_y >= FLOOR_Y:
            self.y = FLOOR_Y - self.ctr_y
            self.is_alive = False
        if self.y - self.ctr_y < 0:
            self.y = self.ctr_y
            self.y_velocity = 0
            self.is_alive = False
        
    def jump(self):
        self.y_velocity = -600
    
    def get_hitbox(self):
        return pygame.Rect(
            self.x - self.ctr_x, 
            self.y - self.ctr_y, 
            self.bird.get_width(), 
            self.bird.get_height()
        )
    
    def animate(self):
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
        surface.blit(self.bird, (self.x - self.ctr_x, self.y - self.ctr_y))