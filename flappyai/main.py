import pygame
from bird import Bird
from config import SCREEN_WIDTH, SCREEN_HEIGHT

def run():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    background = pygame.image.load("./assets/sprites/background.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    bird = Bird(SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2, 1.25)
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

        pygame.display.flip()

        dt = clock.tick(60) / 1000

    pygame.quit()

if __name__ == "__main__":
    run()