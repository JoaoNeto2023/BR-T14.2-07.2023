import pygame
import random
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, CLOUD


class Game:
    def __init__(self):
        pygame.init() #Inicializa a biblioteca do Pygame
        pygame.display.set_caption(TITLE) #Título da janela do jogo
        pygame.display.set_icon(ICON) #Ícone da janela do jogo
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #Superfície de exibição com largura e altura
        self.clock = pygame.time.Clock() #Cria um objeto (Clock) para controlar a taxa de quadros 
        self.playing = False #Determina se o jogo está sendo executado ou não
        self.game_speed = 20 #Define a velocidade do jogo
        self.cloud_speed = 1 #Velocidade do deslocamento das nuvens
        self.x_pos_bg = 0    #Controla a posição do plano de fundo
        self.y_pos_bg = 380  #Controla a posição do plano de fundo
        self.cloud_image = CLOUD
        self.clouds = []
        self.num_clouds = 5
        self.player = Dinosaur()

    def run(self): #Executa o jogo
        for i in range(self.num_clouds):  # num_clouds é o número de nuvens que você deseja adicionar
         cloud_x = random.randint(0, SCREEN_WIDTH)  # Defina a posição x da nuvem aleatoriamente
         cloud_y = random.randint(0, SCREEN_HEIGHT / 2)  # Defina a posição y da nuvem aleatoriamente
         self.clouds.append((cloud_x, cloud_y))
        # Game loop: events - update - draw
        self.playing = True #jogo em andamento, inicia o loop
        while self.playing:
            self.events() #eventos do Pygame - pressionar teclas
            self.update() #atualiza o estado do jogo
            self.draw()   #desenha os elementos do jogo na tela
        pygame.quit()     #finaliza a biblioteca do Pygame

    def events(self): #Processa os eventos do Pygame
        for event in pygame.event.get(): #Verifica se os eventos e, se o tipo de evento for pygame.QUIT, a variável self.playing é False
            if event.type == pygame.QUIT: 
                self.playing = False     #encerrando o jogo

    def update(self): #Utlizado para incrementar a lógica do jogo
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        

    def draw(self):
        self.clock.tick(FPS) #Controla a taxa de quadros do jogo em FPS
        self.screen.fill((255, 255, 255)) #Tela com a cor branca para limpar os desenhos anteriores
        self.draw_background() #chama o método draw_background para desenhar o plano do jogo
        self.player.draw(self.screen) 
        pygame.display.update() #atualiza a janela de exibição com os desenhos
        pygame.display.flip() #atualiza toda a janela de exibição com os desenhos

    def draw_background(self):
        image_width = BG.get_width() #Obtém a largura da imagem de fundo BG e armazena em image_width.
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg)) #Desenha a imagem de fundo BG nas coordenadas 
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg)) #Desenha a imagem de fundo BG novamente na tela, logo após a primeira imagem, criando uma imagem contínua de fundo

        updated_clouds = [] #Cria uma lista vazia para armazenar as novas posições atualizadas das nuvens.

        for cloud in self.clouds: #itera sobre cada nuvem na lista self.clouds
            cloud_x, cloud_y = cloud #Desempacota as coordenadas cloud em cloud_x e cloud_y.
            cloud_x -= self.cloud_speed #Subtrai a velocidade das nuvens 
            if cloud_x < -self.cloud_image.get_width(): #Verifica se a nuvem está completamente fora da tela
                cloud_x = SCREEN_WIDTH #Reposiciona a nuvem no início da tela com uma nova posição vertical aleatória
                cloud_y = random.randint(0, SCREEN_HEIGHT / 2) #Reposiciona a nuvem no início da tela com uma nova posição vertical aleatória
            updated_clouds.append((cloud_x, cloud_y)) #Adiciona as novas coordenadas da nuvem atualizada à lista updated_clouds.
            self.screen.blit(self.cloud_image, (cloud_x, cloud_y)) #Desenha a nuvem na nova posição (cloud_x, cloud_y) na tela.

        self.clouds = updated_clouds #Atualiza a lista self.clouds com as novas posições atualizadas das nuvens.

        self.x_pos_bg -= self.game_speed #Atualiza a posição horizontal do plano de fundo, subtraindo a velocidade do jogo

        if self.x_pos_bg <= -image_width: #Verifica se o plano de fundo está completamente fora da tela
            self.x_pos_bg = 0


        