import random

from dino_runner.utils.constants import SCREEN_WIDTH

class PowerUp:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.rect.y = random.randint(125, 175)
        # tempo em que o power-up é criado
        self.start_time = 0
        
        # duração em segundos
        self.duration = random.randint(5, 10)
    
    def update(self, game_speed, power_ups):
        self.rect.x -= game_speed
        
        if self.rect.x < -self.rect.width:
            power_ups.pop()
            
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))