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
        self.obstacle_manager = ObstacleManager()

        self.death_count = 0
        self.score = 0
        self.score_accumulator = 100
        self.bird_spawn_timer = 10
        self.start_time = pygame.time.get_ticks() / 1000

    def execute(self): #executa o jogo
        self.executing = True
        while self.executing:
            if not self.playing:
                self.display_menu() #chama o menu da tela
                if self.continuing: #continua a partir de um jogo anterior
                    self.continuing = False
                    self.run()
                elif self.resetting: #reinicia o jogo
                    self.resetting = False 
                    self.reset_game() #chamada para reiniciar o jogo
                    self.run() #executa o jogo novamente
        pygame.quit() #encerrar o jogo

    def run(self):
        self.generate_clouds()
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get(): #irá responder as eventos
            if event.type == pygame.QUIT: #verifica se o jogo foi fechado
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN: #verifica se uma tecla foi pressionada
                if event.key == pygame.K_SPACE: #se for o spaço, inicia o jogo
                    self.run()
                elif event.key == pygame.K_c: #se for o c, continua de onde parou
                    self.continuing = True
                    self.playing = False
                elif event.key == pygame.K_r: #se for r, reinicia
                    self.resetting = True
                    self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input) #armazena as teclas pressionadas
        self.obstacle_manager.update(self) #atualiza o comportamento do obstaculo
        self.update_speed() #atualiza a velocidade do jogo
        self.update_score() #atualiza os pontos do jogo

        time_elapsed = pygame.time.get_ticks() / 1000 #o tempo decorrido do pygame iniciado
        if time_elapsed >= self.start_time + self.bird_spawn_timer: #verifica o tempo decorrido, tempo de inicio e temporizador de criação de birds
            self.obstacle_manager.can_spawn_bird = True #armazena a criação de passaros 

    def update_score(self):
        self.score += 1

    def update_speed(self): #atualiza a velocidade do jogo
        if self.score >= 300 and self.game_speed < 30: #verifica a pontuação em relação à velocidade
            self.game_speed += 0.1 #aumenta a velocidade do jogo
        elif self.score >= 200 and self.game_speed < 25:
            self.game_speed += 0.05
        elif self.score >= 100 and self.game_speed < 20:
            self.game_speed += 0.02

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_text("Score: " + str(self.score), 22, (1000, 50)) #exibe a pontuação do jogo na tela
        self.draw_speed() #exibe a velocidade do jogo na tela
        pygame.display.flip() #atualiza a tela em uma área especifica
        pygame.display.update() #atualiza o retangulo da tela

    def draw_speed(self):
        speed_km = int(round(self.game_speed * 10)) #a velocidade do jogo é multiplicada, pega o prox. num inteiro e converte para km/h
        font = pygame.font.Font(FONT_STYLE, 22) #utiliza a fonte e tamanho
        speed_text = font.render(f"Speed: {speed_km} km/h", True, (0, 0, 0)) #texto rederizado e com o km/h (cor preta)
        speed_rect = speed_text.get_rect() #obtem o retangulo do texto
        speed_rect.center = (1000, 80) #posiciona o texto na canto superior direito
        self.screen.blit(speed_text, speed_rect) #desenha o texto na tela

    def draw_text(self, text, size, position):
        font = pygame.font.Font(FONT_STYLE, size)
        text_surface = font.render(text, True, (0, 0, 0)) #contem o texto rederizado, suavizado e de cor preta
        text_rect = text_surface.get_rect() #superficie do texto para facilitar a centralização
        text_rect.center = position #centraliza o texto
        self.screen.blit(text_surface, text_rect) #desenha o texto na tela

    def display_menu(self):
        self.screen.fill((255, 255, 255)) #preencho a tela com branco
        x_text_pos = SCREEN_WIDTH // 2    #centraliza o menu
        y_text_pos = SCREEN_HEIGHT // 2

        font = pygame.font.Font(FONT_STYLE, 22) #instanciei a fonte e o tamanho 
        text = font.render("Press Space to start", True, (0, 0, 0)) #renderizei um texto com suavização ativada e cor preta
        text_rect = text.get_rect() 
        text_rect.center = (x_text_pos, y_text_pos) #define a frase no centro da tela

        continue_text = font.render("Press C to Continue", True, (0, 0, 0))
        continue_rect = continue_text.get_rect()
        continue_rect.center = (x_text_pos, y_text_pos + 30) #posiciona mais abaixo

        reset_text = font.render("Press R to Reset", True, (0, 0, 0))
        reset_rect = reset_text.get_rect()
        reset_rect.center = (x_text_pos, y_text_pos + 60) #posiciona mais abaixo

        self.screen.blit(text, text_rect) #desenhei os textos nas posições da tela
        self.screen.blit(continue_text, continue_rect)
        self.screen.blit(reset_text, reset_rect)

        pygame.display.flip() #atualizei a tela com as alterações do desenho

        self.events() #trás os pressionamentos das teclas
        

    

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

    def generate_clouds(self):
        self.clouds = []
        for i in range(self.num_clouds):
            cloud_x = random.randint(0, SCREEN_WIDTH)
            cloud_y = random.randint(0, SCREEN_HEIGHT / 2)
            self.clouds.append((cloud_x, cloud_y))

    def draw_clouds(self):
        for cloud in self.clouds:
            cloud_x, cloud_y = cloud
            self.screen.blit(self.cloud_image, (cloud_x, cloud_y))

    def reset_game(self):
        self.obstacle_manager.reset_obstacles() #redefine os obstaculos do jogo
        self.player = Dinosaur() #cria um novo objeto
        self.score = 0 #o score vai para 0
        self.game_speed = 20 #a velocidade se mantém 20
        self.clouds.clear() #remove as nuvens para não acumular
        self.generate_clouds() #regenera com novas nuvens

    def continue_game(self):
        self.game_speed = 20
        self.generate_clouds() #regenera as nuvens

    
