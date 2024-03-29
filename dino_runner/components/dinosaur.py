import pygame
from pygame.sprite import Sprite
import pygame.mixer

from dino_runner.utils.constants import DUCKING, HAMMER, HAMMER_TYPE, RUNNING, JUMPING, DEFAULT_TYPE, SHIELD_TYPE, DUCKING_SHIELD,  JUMPING_SHIELD, RUNNING_SHIELD, RUNNING_HAMMER, JUMPING_HAMMER, DUCKING_HAMMER, SOUND_JUMP, SOUND_DEAD
DUCK_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD, HAMMER_TYPE: DUCKING_HAMMER}
JUMP_IMG = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD, HAMMER_TYPE: JUMPING_HAMMER}
RUN_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD, HAMMER_TYPE: RUNNING_HAMMER}


class Dinosaur(Sprite):

    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8.5
    MOVE_SPEED = 5

    def __init__(self):
        
        self.type = DEFAULT_TYPE
        self.image = RUN_IMG[self.type][0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index = 0
        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False
        self.jump_vel = self.JUMP_VEL
        self.setup_state()
        pygame.mixer.init()
        som_jump_path = SOUND_JUMP
        self.som_jump = pygame.mixer.Sound(som_jump_path)

    def setup_state(self):
        self.has_power_up = False
        self.shield = False
        self.show_text = False
        self.shield_time_up = 0

    #Atualiza o estado do Dino   
    def update(self, user_input):
        if self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()
        elif self.dino_duck:
            self.duck()
            
        if user_input[pygame.K_UP] and not self.dino_jump:
            self.dino_jump = True
            self.dino_run = False
            self.dino_duck = False
        elif not self.dino_jump:
            self.dino_run = True
            self.dino_jump = False
            
        if user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
            
        if user_input[pygame.K_RIGHT]:
            self.move_right()
        elif user_input[pygame.K_LEFT]:
            self.move_left()
            
        if self.step_index >= 9: #passos do dino
            self.step_index = 0

    #Atualiza a imagem do Dino
    def run(self):
        self.image = RUN_IMG[self.type][self.step_index // 5] #animação da imagem
        self.dino_rect.y = self.Y_POS
        self.step_index += 1
        
    def jump(self):
        self.image = JUMP_IMG[self.type]
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
            volume = 0.5  # Defina o volume desejado entre 0.0 e 1.0
            self.som_jump.set_volume(volume)
            self.som_jump.play()
            
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_rect.y = self.Y_POS
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
            
    def duck(self):
        self.image = DUCK_IMG[self.type][self.step_index // 5]
        self.dino_rect.y = 350
        self.step_index += 1

    #Move o dino para direita e esquerda   
    def move_right(self):
        self.dino_rect.x += self.MOVE_SPEED
        
    def move_left(self):
        self.dino_rect.x -= self.MOVE_SPEED

    #Desenha o dino na tela        
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
