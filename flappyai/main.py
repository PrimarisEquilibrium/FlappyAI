import pygame
import pygame_gui
import neat
import sys
import pickle
from bird import Bird
from pipe import PipeManager
from ground import GroundManager
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from utils import display_text

background = pygame.image.load("./assets/sprites/background.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

generation = 0
spawn_initial_pipe = True
best_score = 0
def run(genomes, config):
    global generation, spawn_initial_pipe, best_score
    nets = []
    birds = []
    score = 0

    for id, genome in genomes:
        # Create a neural network from]\ the gene
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0 # Set initial fitness value to 0

        birds.append(Bird(SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2))

    # Pygame initialization
    pygame.init()
    pygame.display.set_caption("FlappyAI")
    pygame.display.set_icon(pygame.image.load("./assets/sprites/bird.png"))

    # Pygame variables
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
    save_network_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((15, SCREEN_HEIGHT - 65), (150, 50)),
        text='Save Network',
        manager=manager
    )
    load_network_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((175, SCREEN_HEIGHT - 65), (150, 50)),
        text='Load Network',
        manager=manager
    )

    ground_manager = GroundManager()
    ground_manager.create_ground()

    pipe_manager = PipeManager()
    if spawn_initial_pipe:
        pipe_manager.spawn_pipe()
        spawn_initial_pipe = False

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
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == save_network_button:
                    with open('data', 'wb') as data_file:
                        pickle.dump([nets, best_score, generation], data_file)
                if event.ui_element == load_network_button:
                    with open('data', 'rb') as data_file:
                        data = pickle.load(data_file)
                        nets, best_score, generation = data[0], data[1], data[2]
            manager.process_events(event)

        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        # Input data and get results from network
        closest_pipe = pipe_manager.get_closest_pipe(birds[0].x)
        for i, bird in enumerate(birds):
            if closest_pipe:
                output = nets[i].activate([
                    bird.y_velocity,
                    closest_pipe.x - bird.x,
                    bird.y - closest_pipe.top_pipe_y + closest_pipe.top_pipe.get_height(),
                    bird.y - closest_pipe.bottom_pipe_y,
                ])
                if output[0] > 0.5:
                    bird.jump()
          
        # Update birds and fitness
        remaining_birds = 0
        for i, bird in enumerate(birds):
            if bird.is_alive:
                remaining_birds += 1
                bird.update(dt)
                genomes[i][1].fitness += 0.1

                if pipe_manager.has_passed_pipe(bird):
                    score += 1

                if bird.has_collided(pipe_manager):
                    genomes[i][1].fitness -= 3
                
                if bird.is_out_of_bounds():
                    genomes[i][1].fitness -= 5
            
        if remaining_birds == 0:
            generation += 1
            if score > best_score:
                best_score = score
            break

        pipe_manager.draw_pipes(screen)
        ground_manager.draw(screen)

        for bird in birds:
            if bird.is_alive:
                bird.animate()
                bird.draw(screen)

        pipe_manager.update_pipes(dt)
        ground_manager.update(dt)
        
        display_text(screen, f"Gen: {generation}", 36, "white", 20, 20)
        display_text(screen, f"Alive: {remaining_birds}", 36, "white", 20, 50)
        display_text(screen, f"Score: {score}", 36, "white", 20, 80)
        display_text(screen, f"Best: {best_score}", 36, "white", 20, 110)

        manager.update(dt)
        manager.draw_ui(screen)

        pygame.display.flip()

        dt = clock.tick(60) / 1000

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

    p.run(run, 300)