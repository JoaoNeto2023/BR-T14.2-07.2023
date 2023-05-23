import random
from tkinter import S

from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import LARGE_CACTUS, SMALL_CACTUS

class Cactus(Obstacle):
    def __init__(self, image_small):
        super().__init__(image_small, 0)  # Passando o valor 0 como argumento para o parâmetro 'type' do cactus pequeno
        self.rect.y = 325  # Coordenada y padrão para o cactus pequeno







