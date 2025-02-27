import pygame
import neat
import sys
from bird import Bird
from pipe import PipeManager
from ground import GroundManager
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FLOOR_Y
from utils import display_text

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

def run(genomes, config):
    nets = []
    birds = []

    for id, genome in genomes:
        # Create a neural network from the gene
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0 # Set initial fitness value to 0

        birds.append(Bird(SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2))

    # Pygame initialization
    pygame.init()
    pygame.display.set_caption("FlappyAI")
    pygame.display.set_icon(pygame.image.load("./assets/sprites/bird.png"))
    pygame.mouse.set_visible(0)

    # Pygame variables
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    ground_manager = GroundManager()
    ground_manager.create_ground()

    pipe_manager = PipeManager()
    
    time = 0

    # Game loop
    while True:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    return

        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        # Input data and get results from network
        closest_pipe = pipe_manager.get_closest_pipe(birds[0].x)
        for i, bird in enumerate(birds):
            if closest_pipe:
                output = nets[i].activate([
                    bird.y_velocity,
                    FLOOR_Y - bird.y,
                    closest_pipe.x - bird.x,
                    closest_pipe.top_pipe_y + closest_pipe.top_pipe.get_height(),
                    closest_pipe.bottom_pipe_y
                ])
                i = output.index(max(output))
                if i == 1:
                    bird.jump()
        
        
        # Update birds and fitness
        remaining_birds = 0
        for i, bird in enumerate(birds):
            if bird.is_alive:
                remaining_birds += 1
                bird.update(dt)
                genomes[i][1].fitness += 0.05

                if pipe_manager.has_passed_pipe(bird):
                    genomes[i][1].fitness += 10  

                if bird.has_collided(pipe_manager):
                    genomes[i][1].fitness -= 5
                
                if bird.is_out_of_bounds():
                    genomes[i][1].fitness -= 10
            
        if remaining_birds == 0:
            print(time, pygame.time.get_ticks() - time)
            time = pygame.time.get_ticks()
            break

        pipe_manager.draw_pipes(screen)
        ground_manager.draw(screen)

        for bird in birds:
            if bird.is_alive:
                bird.animate()
                bird.draw(screen)

        pipe_manager.update_pipes(dt)
        ground_manager.update(dt)
        
        # display_text(screen, str(score), 72, "white", 20, 20)

        pygame.display.flip()

        dt = clock.tick(240) / 1000

if __name__ == "__main__":
    # Create NEAT configuration
    config_path = "./config/config-feedforward.txt"
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Create core evolution algorithm class
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    p.run(run, 300)