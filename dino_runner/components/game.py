import pygame
import random
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, CLOUD
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from pygame import font

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.cloud_speed = 1
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.cloud_image = CLOUD
        self.clouds = []
        self.num_clouds = 10
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.death_count = 0
        self.score = 0
        self.score_accumulator = 100
        self.bird_spawn_timer = 10
        self.start_time = pygame.time.get_ticks() / 1000

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

        pygame.display.quit()
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
        self.obstacle_manager.update(self)
        self.update_score()

        time_elapsed = pygame.time.get_ticks() / 1000
        if time_elapsed >= self.start_time + self.bird_spawn_timer:
            self.obstacle_manager.can_spawn_bird = True

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 2

        if self.score >= self.score_accumulator:
            self.score_accumulator = self.score

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.format_text(f"Score: {self.score}", 1000, 50, 30)
        pygame.display.update()
        pygame.display.flip()

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
        for i in range(self.num_clouds):
            cloud_x = random.randint(0, SCREEN_WIDTH)
            cloud_y = random.randint(0, SCREEN_HEIGHT / 2)
            self.clouds.append((cloud_x, cloud_y))

    def draw_clouds(self):
        for cloud in self.clouds:
            cloud_x, cloud_y = cloud
            self.screen.blit(self.cloud_image, (cloud_x, cloud_y))

    def format_text(self, text, x, y, size):
        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def show_menu(self):
        pass

