import pygame
from bird import Bird
from pipe import PipeManager
from ground import GroundManager
from config import SCREEN_WIDTH, SCREEN_HEIGHT

background = pygame.image.load("./assets/sprites/background.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

def run():
    # Pygame initialization
    pygame.init()
    pygame.display.set_caption("FlappyAI")
    pygame.display.set_icon(pygame.image.load("./assets/sprites/bird.png"))
    pygame.mouse.set_visible(0)

    # Pygame variables
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    hasStarted = False
    running = True
    dt = 0

    # Game class initialization
    bird = Bird(SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2, 1.8)

    ground_manager = GroundManager()
    ground_manager.create_ground()

    pipe_manager = PipeManager()

    # Game loop
    while running:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
                hasStarted = True
                bird.jump()

        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
    
        pipe_manager.draw_pipes(screen)
        ground_manager.draw(screen)
        bird.draw(screen)

        if hasStarted:
            pipe_manager.update_pipes(dt)
            ground_manager.update(dt)
            bird.update(dt)
        
        print(pipe_manager.has_bird_collided(bird.get_hitbox()))

        pygame.display.flip()

        dt = clock.tick(240) / 1000

    pygame.quit()

if __name__ == "__main__":
    run()