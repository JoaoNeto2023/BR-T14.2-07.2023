import pygame
from pygame.sprite import Sprite
from dino_runner.utils.constants import SCREEN_WIDTH

class Obstacle(Sprite):
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.get_obstacle_rect()
        self.rect.x = SCREEN_WIDTH

    def get_obstacle_rect(self): #retorna um retangulo que represnta a posição e o tamanho do obstaculo
        if self.type < len(self.image): 
            return self.image[self.type].get_rect() #o rentangulo é obtido a partir da imagem do tipo do obstaculo
        else:
            return pygame.Rect(0, 0, 0, 0) #retorna um retangulo vazio

    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed #o SCREEN_WIDHT é diminuído pela velocidade do jogo, fazendo com que ele siga a tela

        if self.rect.x < -self.rect.width: 
            obstacles.pop()       #remove o obstaculo da tela.

    def draw(self, screen): #desenhando o obstaculo no jogo
        if self.type < len(self.image):
            screen.blit(self.image[self.type], (self.rect.x, self.rect.y))




