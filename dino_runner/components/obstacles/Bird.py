import random
from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import BIRD

class Bird(Obstacle):
    def __init__(self, image, bird_y):
        self.type = random.randint(0, 1)
        super().__init__(image, self.type)
        if bird_y == 0: #identifica se a posição y do pássaro é 0
            self.rect.y = 260 #atualiza a posição do pássaro
        else:
            self.rect.y = 315 #se não for 0, atualiza para 315
        
        self.step_index = 0 #controla a animação do pássaro
        self.direction = 2  #define a direção inicial do pássaro para cima (2)
        
    def draw(self, screen):
        if self.step_index >= 9: #verifica se o índice é maior ou igual a 9
            self.step_index = 0 #se for, atualiza para 0, fazendo com que o pássaro passe a impressão de voo
        screen.blit(self.image[self.step_index//5], self.rect) #desenha a imagem
        self.step_index += 1 #incrementa o indice para avançar na animação
        
        self.rect.y += self.direction #atualiza a posição y do retângulo do pássaro peseado na direção atual. 
        
        if self.rect.y <= 260:  #verifica se a posição é menor ou igual a 260
            self.direction = 2  #define o pássaro para subir
        elif self.rect.y >= 315: #se for maior ou igual a 315 
            self.direction = -2 #define para o pássaro descer



