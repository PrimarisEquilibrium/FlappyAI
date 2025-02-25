import pygame
from bird import Bird
from pipe import PipeManager
from ground import GroundManager
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from utils import display_text, Button

background = pygame.image.load("./assets/sprites/background.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

def display_game_over_screen(surface, score):
    pygame.mouse.set_visible(1)

    game_over_screen_fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_over_screen_fade.fill((0, 0, 0))
    game_over_screen_fade.set_alpha(160)
    surface.blit(game_over_screen_fade, (0, 0))

    display_text(surface, "Game Over!", 72, "white", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 75, True)
    display_text(surface, f"Score: {score}", 36, "white", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, True)
    display_text(surface, f"High Score: N/A", 36, "white", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50, True)
    display_text(surface, f"Press any key to play again", 36, "white", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 100, True)

def run():
    # Pygame initialization
    pygame.init()
    pygame.display.set_caption("FlappyAI")
    pygame.display.set_icon(pygame.image.load("./assets/sprites/bird.png"))
    pygame.mouse.set_visible(0)

    # Pygame variables
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    # Game class initialization
    bird = Bird(SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2, 1.8)

    ground_manager = GroundManager()
    ground_manager.create_ground()

    pipe_manager = PipeManager()

    score = 0

    # Game loop
    has_started = False
    game_over = False
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
                has_started = True
                if not game_over:
                    bird.jump()
            if game_over and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
                run() # Replay the game

        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
    
        pipe_manager.draw_pipes(screen)
        ground_manager.draw(screen)
        bird.draw(screen)

        if pipe_manager.is_game_over(bird.get_hitbox()):
            game_over = True

        if has_started:
            bird.animate()
            if not game_over:
                pipe_manager.update_pipes(dt)
                ground_manager.update(dt)
            if bird.update(dt) == False:
                game_over = True
        
        if pipe_manager.has_passed_pipe(bird.get_hitbox()):
            score += 1
        
        display_text(screen, str(score), 72, "white", 20, 20)

        if game_over:
            display_game_over_screen(screen, score)

        pygame.display.flip()

        dt = clock.tick(240) / 1000

    pygame.quit()

if __name__ == "__main__":
    run()