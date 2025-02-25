import pygame
import random
from bird import Bird
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Pipe:
    def __init__(self, x):
        self.x = x
        self.opening = random.randint(25, int(SCREEN_HEIGHT - 25)) # The point where the pipe is open
        self.opening_size = 100
    
    def draw(self, surface):
        top_pipe = pygame.image.load("./assets/sprites/pipe.png")
        top_pipe = pygame.transform.scale_by(top_pipe, 1.5)
        bottom_pipe = pygame.transform.rotate(top_pipe, 180)
        surface.blit(top_pipe, (self.x, self.opening + self.opening_size))
        surface.blit(bottom_pipe, (self.x, self.opening - self.opening_size - bottom_pipe.get_height()))

class PipeSpawner:
    def __init__(self):
        self.pipes = []

def run():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    background = pygame.image.load("./assets/sprites/background.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    pipe = Pipe(100)

    bird = Bird(SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2, 1.5)
    pygame.mouse.set_visible(0)
    while running:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        bird.draw(screen)
        bird.update(event_list, dt)

        pipe.draw(screen)

        pygame.display.flip()

        dt = clock.tick(60) / 1000

    pygame.quit()

if __name__ == "__main__":
    run()