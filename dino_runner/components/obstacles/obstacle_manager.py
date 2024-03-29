import random
import pygame

from dino_runner.components.obstacles.cactus import Cactus
import pygame.mixer
from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.components.obstacles.Bird import Bird
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD, GAME_OVER, DINO_DEAD, SOUND_DEAD


class ObstacleManager:
    def __init__(self):
        self.obstacles = []  # lista usada para armazenar os obstáculos
        self.spawn_bird = False  # Controle para gerar pássaros
        pygame.mixer.init()
        som_death_path = SOUND_DEAD
        self.som_dead = pygame.mixer.Sound(som_death_path)

    def update(self, game):
        if len(self.obstacles) == 0:
            if game.score < 500 or random.choice([True, False]):  # Verifica a pontuação ou escolhe aleatoriamente
                obstacle_type = random.choice([SMALL_CACTUS, LARGE_CACTUS])  # seleciona aleatoriamente qual obstáculo deve vir
                self.obstacles.append(Cactus(obstacle_type))  # adiciona um objeto à lista de obstáculos
                self.spawn_bird = True  # Define o controle para gerar pássaros após o próximo obstáculo cacto
            else:  # Gera pássaros após atingir 500
                bird_y = random.randint(0, 1)  # seleciona aleatoriamente a posição do pássaro entre 0 e 1.
                self.obstacles.append(Bird(BIRD, bird_y))
                self.spawn_bird = False  # indica que não é necessário gerar um pássaro.

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)  # passa a velocidade do jogo e a lista de obstáculos como parâmetros, chamando cada obstáculo
            if game.player.dino_rect.colliderect(obstacle.rect):  # verifica a colisão entre o dinossauro e os obstáculos
                if not game.player.has_power_up:  # verifica se o jogador não tem um power-up
                    self.game_over(game.screen, game.player)  # chama o método game_over para exibir a mensagem "GAME OVER"
                    game.playing = False  # para o jogo
                    game.death_count += 1  # valida a quantidade de mortes
                    self.reset_obstacles()  # redefine a lista de obstáculos
                else:
                    self.obstacles.remove(obstacle)  # remove o obstáculo da lista de obstáculos se o jogador tiver um power-up

    def draw(self, screen):  # desenha o obstáculo na tela
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):  # redefine a lista de obstáculos como vazia
        self.obstacles.clear()

    def game_over(self, screen, player):
        screen_rect = screen.get_rect()
        game_over_image = GAME_OVER
        game_over_rect = game_over_image.get_rect(center=screen_rect.center)
        screen.blit(game_over_image, game_over_rect)
        volume = 0.5  # Defina o volume desejado entre 0.0 e 1.0
        self.som_dead.set_volume(volume)
        self.som_dead.play()
        player.is_dead = True  # Define o estado do dinossauro como morto
        player.dino_image = DINO_DEAD  # Altera a imagem do dinossauro para a imagem do dinossauro morto
        player.dino_rect = player.dino_image.get_rect()  # Atualiza o retângulo de colisão do dinossauro com a nova imagem
        pygame.display.update()
        pygame.time.delay(1500)
        








