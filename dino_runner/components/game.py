import pygame
import random
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, CLOUD, FONT_STYLE, DEFAULT_TYPE, COLOR
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager



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
        self.running = True
        self.background_color = (255, 255, 255)  # Cor de fundo inicial (branco)
        self.color_counter = 0  # Contador de cores
        self.colors = COLOR

        self.game_speed = 20
        self.cloud_speed = 1

        self.x_pos_bg = 0
        self.y_pos_bg = 380

        self.cloud_image = CLOUD
        self.num_clouds = 10

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

        self.death_count = 0
        self.score = 0
        self.score_accumulator = 100
        self.bird_spawn_timer = 10
        self.start_time = pygame.time.get_ticks() / 1000

    #Método para execução do jogo
    def execute(self): 
        self.executing = True
        while self.executing and self.running:
            if not self.playing:
                self.display_menu() #chama o menu da tela
                if self.continuing: #continua a partir de um jogo anterior
                    self.continuing = False
                    self.run()
                elif self.resetting: #reinicia o jogo
                    self.resetting = False 
                    self.reset_game() 
                    self.run() #executa o jogo novamente
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #verifica se o jogo foi fechado
                    self.executing = False
                    self.playing = False
        pygame.quit() #encerrar o jogo
        
    #Método de atualização do jogo
    def run(self):
        self.generate_clouds()
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    #Método de controle de eventos
    def events(self):
        for event in pygame.event.get(): #irá responder as eventos
            if event.type == pygame.QUIT: 
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE: 
                    self.run()
                elif event.key == pygame.K_c: 
                    self.continuing = True
                    self.playing = False
                elif event.key == pygame.K_r: 
                    self.resetting = True
                    self.playing = False
    #Metodo responsável por atualizar o estado do jogo
    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input) #armazena as teclas pressionadas
        self.obstacle_manager.update(self) #atualiza o comportamento do obstaculo
        self.power_up_manager.update(self)
        self.update_speed() 
        self.update_score() 

        time_elapsed = pygame.time.get_ticks() / 1000 #o tempo decorrido
        if time_elapsed >= self.start_time + self.bird_spawn_timer: #verifica o tempo decorrido, tempo de inicio e temporizador de criação de birds
            self.obstacle_manager.can_spawn_bird = True #armazena a criação de passaros 
    #Método de atualização do score
    def update_score(self):
        self.score += 1 
        if self.score % 250 == 0: #multiplo de 250
            self.background_color = random.choice(self.colors)
            self.color_counter += 1
    
            if self.color_counter == 8:
                self.color_counter = 0
    #Método deatualização da velocidade 
    def update_speed(self): 
        if self.score >= 300 and self.game_speed < 30: #verifica a pontuação em relação à velocidade
            self.game_speed += 0.1 #aumenta a velocidade do jogo
        elif self.score >= 200 and self.game_speed < 25:
            self.game_speed += 0.05
        elif self.score >= 100 and self.game_speed < 20:
            self.game_speed += 0.02

    #método para desenhar o tempo restante do power_up ativado
    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time_up - pygame.time.get_ticks())/1000, 2)
            if time_to_show >= 0:
                font = pygame.font.Font(FONT_STYLE, 22)
                text = font.render(f"Power Up Time:{time_to_show}s", True, (255,0,0))
                text_rect = text.get_rect()
                text_rect.x = 500
                text_rect.y = 50
                self.screen.blit(text, text_rect)    
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    #método para desenhar os jogos na tela
    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill(self.background_color)  # Preenche o fundo com a cor atual
        #self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)  
        self.draw_power_up_time()
        self.draw_speed()
        self.draw_text("Score: " + str(self.score), 22, (1000, 50))
        pygame.display.flip()
        pygame.display.update()

    #Método para desenhar a velocidade
    def draw_speed(self):
        speed_km = int(round(self.game_speed * 10)) #a velocidade do jogo é multiplicada, pega o prox. num inteiro e converte para km/h
        font = pygame.font.Font(FONT_STYLE, 22) 
        speed_text = font.render(f"Speed: {speed_km} km/h", True, (0, 0, 0)) 
        self.draw_text("Score: " + str(self.score), 22, (1000, 50)) 
        speed_rect = speed_text.get_rect() 
        speed_rect.center = (1000, 80) 
        self.screen.blit(speed_text, speed_rect) 

    #método para desenhar os Textos
    def draw_text(self, text, size, position):
        font = pygame.font.Font(FONT_STYLE, size)
        text_surface = font.render(text, True, (0, 0, 0)) 
        text_rect = text_surface.get_rect() 
        text_rect.center = position 
        self.screen.blit(text_surface, text_rect) #desenha o texto na tela

    #Método para desenhar o menu
    def display_menu(self):
        self.screen.fill((255, 255, 255)) 
        x_text_pos = SCREEN_WIDTH // 2    #centraliza o menu
        y_text_pos = SCREEN_HEIGHT // 2

        font = pygame.font.Font(FONT_STYLE, 22) #instanciei a fonte e o tamanho 
        text = font.render("Press Space to start", True, (0, 0, 0)) #renderizei um texto com suavização ativada e cor preta
        text_rect = text.get_rect() 
        text_rect.center = (x_text_pos, y_text_pos) 

        continue_text = font.render("Press C to Continue", True, (0, 0, 0))
        continue_rect = continue_text.get_rect()
        continue_rect.center = (x_text_pos, y_text_pos + 30) 

        reset_text = font.render("Press R to Reset", True, (0, 0, 0))
        reset_rect = reset_text.get_rect()
        reset_rect.center = (x_text_pos, y_text_pos + 60) 

        self.screen.blit(text, text_rect) 
        self.screen.blit(continue_text, continue_rect)
        self.screen.blit(reset_text, reset_rect)

        pygame.display.flip() #atualizei a tela com as alterações do desenho
        self.events() #trás os pressionamentos das teclas

    #Método para desenhar o plano do jogo
    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        self.update_clouds()
        self.draw_clouds()
        if self.x_pos_bg <= -image_width:
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
        
    #Método para atualizar as nuvens
    def update_clouds(self):
        updated_clouds = []

        for cloud in self.clouds:
            cloud_x, cloud_y = cloud
            cloud_x -= self.cloud_speed
            if cloud_x < -self.cloud_image.get_width():
                cloud_x = SCREEN_WIDTH #reposiciona a nuvem à direita da tela. 
                cloud_y = random.randint(0, SCREEN_HEIGHT / 2)
            updated_clouds.append((cloud_x, cloud_y))
            self.screen.blit(self.cloud_image, (cloud_x, cloud_y)) #Desenha a nuvem
        self.clouds = updated_clouds

    #Método para gerar lista de coordenadas para as nuvens
    def generate_clouds(self):
        self.clouds = []
        for i in range(self.num_clouds):
            cloud_x = random.randint(0, SCREEN_WIDTH)
            cloud_y = random.randint(0, SCREEN_HEIGHT / 2) #metade superior da tela
            self.clouds.append((cloud_x, cloud_y))

    #Método para desenhar as nuvens
    def draw_clouds(self):
        for cloud in self.clouds:
            cloud_x, cloud_y = cloud
            self.screen.blit(self.cloud_image, (cloud_x, cloud_y))

    #Método para resetar o jogo
    def reset_game(self):
        self.obstacle_manager.reset_obstacles() #redefine os obstaculos do jogo
        self.power_up_manager.reset_power_ups()
        self.player = Dinosaur() #cria um novo objeto
        self.score = 0 #o score vai para 0
        self.game_speed = 20 
        self.clouds.clear() #remove as nuvens para não acumular
        self.generate_clouds() #regenera com novas nuvens
    #Método para continuar o jogo 
    def continue_game(self):
        self.game_speed = 20
        self.generate_clouds() #regenera as nuvens

    
