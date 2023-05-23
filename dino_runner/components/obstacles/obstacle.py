import pygame
from pygame.sprite import Sprite
from dino_runner.utils.constants import SCREEN_WIDTH

class Obstacle(Sprite):
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.get_obstacle_rect()
        self.rect.x = SCREEN_WIDTH

    def get_obstacle_rect(self):
        if self.type < len(self.image):
            return self.image[self.type].get_rect()
        else:
            return pygame.Rect(0, 0, 0, 0)

    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed

        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, screen):
        if self.type < len(self.image):
            screen.blit(self.image[self.type], (self.rect.x, self.rect.y))




