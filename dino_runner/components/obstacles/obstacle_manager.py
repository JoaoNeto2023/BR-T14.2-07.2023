import random
import pygame

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.components.obstacles.Bird import Bird
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD, GAME_OVER


class ObstacleManager:
    def __init__(self):
        self.obstacles = [] #lista usada para armazenar os obstaculos
        self.spawn_bird = False  # Controle para gerar pássaros

    def update(self, game):
        if len(self.obstacles) == 0:
            if game.score < 900 or random.choice([True, False]):  # Verifica a pontuação ou escolhe aleatoriamente
                obstacle_type = random.choice([SMALL_CACTUS, LARGE_CACTUS]) #seleciona aleatoriamente qual obstaculo deve vir
                self.obstacles.append(Cactus(obstacle_type)) #adiciona um objeto à lista de obstaculos
                self.spawn_bird = True  # Define o controle para gerar pássaros após o próximo obstáculo cacto
            else:  # Gera pássaros após atingir 900
                bird_y = random.randint(0, 1) #seleciona aleatoriamente a posição do pássaro entre 0, 1.
                self.obstacles.append(Bird(BIRD, bird_y)) 
                self.spawn_bird = False #indica que não é necessário gerar um pássaro.
        
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles) #passa a velocidade do jogo e a lista de obstáculos como parâmetros, chamando cada obstaculo
            if game.player.dino_rect.colliderect(obstacle.rect): #verifica o choque entre o dino e os obstaculos
                if not game.player.has_power_up: #verifica se o jogo n tem um power-up
                    game.screen.blit(GAME_OVER, (200, 250)) #desenha a imagem game-over
                    pygame.display.update() #atualiza a tela do jogo
                    pygame.time.delay(1500) #faz uma pausa de 1,5 segundos. A pausa serve para exibir o texto
                    game.playing = False    #para o jogo
                    game.death_count += 1   #valida a quantidade de mortes
                    self.reset_obstacles()  #redefine a lista de obstaculos
                else:
                    self.obstacles.remove(obstacle) #aqui irá remover o obstaculo da lista de obstaculo se o jogador tiver um power-up

    def draw(self, screen): #desenha o obstaculo na tela
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self): #redefine a lista de obstaculos como vazia
        self.obstacles = []






