import pygame
import random
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, CLOUD, FONT_STYLE 
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        

        self.playing = False
        self.executing = False
        self.continuing = False
        self.resetting = False


        self.game_speed = 20
        self.cloud_speed = 1
        

        self.x_pos_bg = 0
        self.y_pos_bg = 380

        self.cloud_image = CLOUD
        self.num_clouds = 10

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager() #instancia a classe ObstacleManager para gerenciar os obstaculos 

        self.death_count = 0 #armazena o numero de mortes do jogador
        self.score = 0       # armazena a pontuação do jogo

        self.score_accumulator = 100 #define o valor para acumular pontos antes de aumentar a velocidade do jogo
        self.bird_spawn_timer = 10   #define o tempo(seg) para o próximo pássaro aparecer
        self.start_time = pygame.time.get_ticks() / 1000 #armazena o tempo de início do jogo em segundos
        

    def execute(self):
        self.executing = True
        while self.executing:
            
            if not self.playing:
                self.display_menu()
        
        pygame.quit()    

    def run(self):
        self.generate_clouds()
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self) #atualiza o status dos obstaculos
        self.update_speed()
        self.update_score() #atualiza a pontuação e a velocidade do jogo

        time_elapsed = pygame.time.get_ticks() / 1000 #calcula o tempo passado do jogo a partir do início(seg)
        if time_elapsed >= self.start_time + self.bird_spawn_timer: #condição indicando que se o tempo for maior ou igual ao tempo de início + o temporizador de aparição de passaros
            self.obstacle_manager.can_spawn_bird = True #habilita verdadeiro para o aparecimento de 1 pássaro

    def update_score(self):
        self.score += 1

    def update_speed(self):
       if self.score >= 300 and self.game_speed < 30:
           self.game_speed += 0.1  # Aumenta a velocidade em 0.1 quando o score ultrapassar 300 até atingir o limite máximo de 30
       elif self.score >= 200 and self.game_speed < 25:
           self.game_speed += 0.05  # Aumenta a velocidade em 0.05 quando o score ultrapassar 200 até atingir o limite máximo de 25
       elif self.score >= 100 and self.game_speed < 20:
           self.game_speed += 0.02  # Aumenta a velocidade em 0.02 quando o score ultrapassar 100 até atingir o limite máximo de 20

        

    def draw(self): #Melhorar o codigo para os textos que sejam mais reutilizaveis
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_text("Score: " + str(self.score), 22, (1000, 50))
        self.draw_text("Speed: " + str(int(round(self.game_speed * 10))) + " km/h", 22, (1000, 80))
        pygame.display.flip()
        pygame.display.update()
    
    def draw_speed(self): #Metodo criado para colocar a velocidade do jogo em km/h
        speed_km = int(round(self.game_speed * 10))  # Multiplica a velocidade por 10 para exibir em km/h
        font = pygame.font.Font(FONT_STYLE, 22)
        speed_text = font.render(f"Speed: {speed_km} km/h", True, (0, 0, 0))
        speed_rect = speed_text.get_rect()
        speed_rect.center = (1000, 80)

        self.screen.blit(speed_text, speed_rect)

    def draw_text(self, text, size, position):
        font = pygame.font.Font(FONT_STYLE, size)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = position
        self.screen.blit(text_surface, text_rect)

    def display_menu(self):
        self.screen.fill((255, 255, 255))
        x_text_pos = SCREEN_WIDTH//2
        y_text_pos = SCREEN_HEIGHT//2

        font = pygame.font.Font(FONT_STYLE, 22)
        text = font.render("Press any key to start", True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (x_text_pos, y_text_pos)
        
        self.screen.blit(text, text_rect)
        print(self.death_count)
        
        self.menu_events_handler()
        pygame.display.flip()

    def menu_events_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.executing = False
                self.playing = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def draw_score(self):
        
        font = pygame.font.Font(FONT_STYLE, 22)
        text = font.render(f"Score: {self.score}", True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (1000,50)
        
        self.screen.blit(text, text_rect)
        

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        self.update_clouds()
        self.draw_clouds()
        if self.x_pos_bg <= -image_width:
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def update_clouds(self):
        updated_clouds = []

        for cloud in self.clouds:
            cloud_x, cloud_y = cloud
            cloud_x -= self.cloud_speed
            if cloud_x < -self.cloud_image.get_width():
                cloud_x = SCREEN_WIDTH
                cloud_y = random.randint(0, SCREEN_HEIGHT / 2)
            updated_clouds.append((cloud_x, cloud_y))
            self.screen.blit(self.cloud_image, (cloud_x, cloud_y))
        self.clouds = updated_clouds

    def generate_clouds(self): #gera as nuvens para inicio do jogo
        self.clouds = []
        for i in range(self.num_clouds): #gera as nuvens aleatoriamente
            cloud_x = random.randint(0, SCREEN_WIDTH)
            cloud_y = random.randint(0, SCREEN_HEIGHT / 2)
            self.clouds.append((cloud_x, cloud_y))

    def draw_clouds(self): #desenha as nuvens na tela
        for cloud in self.clouds: #intera sobre todas as nunvens da tela
            cloud_x, cloud_y = cloud
            self.screen.blit(self.cloud_image, (cloud_x, cloud_y)) #desenha as nuvens na tela baseada nas suas coordenadas

    def reset_game(self):
        self.obstacle_manager.reset_obstacles()
        self.player = Dinosaur()
        self.score = 0
        self.game_speed = 20
        self.clouds.clear() #limpo as nuvens
        self.generate_clouds() #gera novas nuvens

    def continue_jogo(self):
     self.game_speed = 20
     self.generate_clouds()

    
