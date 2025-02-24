import pygame

# Represents the "flappy" bird
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vertical_speed = 500
        self.falling_constant = 5
        self.jump_speed = 10
    
    def update(self, event_list, dt):
        for event in event_list:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.y -= 100
        self.y += 7
    
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

    bird = Bird(50, 50)
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