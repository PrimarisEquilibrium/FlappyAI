import pygame
from bird import Bird
from pipe import PipeManager
from ground import GroundManager
from config import SCREEN_WIDTH, SCREEN_HEIGHT

def run():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    background = pygame.image.load("./assets/sprites/background.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    ground_manager = GroundManager()
    ground_manager.create_ground()

    ACTION = pygame.event.custom_type()
    pipe_manager = PipeManager()

    pipe_manager.spawn_pipe()
    pygame.time.set_timer(pygame.event.Event(ACTION, action=pipe_manager.spawn_pipe), 1500, 100)

    bird = Bird(SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2, 1.8)
    pygame.mouse.set_visible(0)
    while running:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
            if event.type == ACTION:
                event.action()

        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        pipe_manager.update_pipes(dt)
        pipe_manager.draw_pipes(screen)

        ground_manager.update(dt)
        ground_manager.draw(screen)

        bird.draw(screen)
        bird.update(event_list, dt)

        pygame.display.flip()

        dt = clock.tick(240) / 1000

    pygame.quit()

if __name__ == "__main__":
    run()