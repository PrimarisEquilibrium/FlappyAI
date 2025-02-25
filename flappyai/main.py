import pygame

# Represents the "flappy" bird
class Bird:
    def __init__(self, x, y, bird_size):
        self.x = x
        self.y = y
        self.bird_size = bird_size

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
    
    def jump(self):
        pass
    
    def draw(self, surface):
        pygame.draw.circle(surface, "yellow", (self.x, self.y), 25)

def run():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    bird = Bird(50, 50, 25)
    while running:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False

        screen.fill("purple")

        bird.draw(screen)
        bird.update(event_list, dt)

        pygame.display.flip()

        dt = clock.tick(60) / 1000

    pygame.quit()

if __name__ == "__main__":
    run()