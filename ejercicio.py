import pygame
import random
import sys
#comentario nuevo
pygame.init()
pygame.mixer.init()

#pantalla principal 
WIDTH, HEIGHT = 900, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Code Jump')
CLOCK = pygame.time.Clock()
FPS = 60 

WHITE = (255, 255, 255)
BACK = (41, 90, 97)
RED = (220, 50, 50)
GREEND = (40, 180, 80)

FONT = pygame.font.SysFont(None, 28)
BIG_FONT = pygame.font.SysFont(None, 60)

GRAVITY = 1
GROUND_Y = HEIGHT - 80

MAX_LEVELS = 3

#Ccargar imagurnes
def load_image(path, size):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    except:
        surf = pygame.Surface(size)
        surf.fill((150, 150, 150))
        return surf 
    
def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except:
        return None 
    
PLAYER_IMG = load_image("player.png",(50, 60))
ENEMY_IMG = load_image("enemy.png",(50, 50))
COIN_IMG = load_image("coin.png",(30, 30))
GOAL_IMG = load_image("goal.png",(150, 150))

BG_IMAGES =
    load_image('background1.jpg', (WIDTH, HEIGHT))
    load_image('background2.jpg', (WIDTH, HEIGHT))
    load_image('background3.jpg', (WIDTH, HEIGHT))
     
JUMP_SOUND = load_sound('jump.wav')
HIT_SOUND = load_sound('hit.wav')
COIN_SOUND = load_sound('coin.wav')

#musica de fondo
def start_screen():
    while True:
        SCREEN.fill(BACK)
        title = BIG_FONT.render("CODE JUMP", True, WHITE)
        msg = FONT.render("FLECHA IZQUIERDA - FLECHA DERECHA mover / ESPACIO saltar", True, WHITE)
        msg1 = FONT.render("Desarrollado por: Xiomara Lozada", True, WHITE)
        start = FONT.render("Presiona ENTER para comenzar", True, WHITE)

        SCREEN.blit(title,(WIDTH//2 - title.get_width()//2, 160))
        SCREEN.blit(msg,(WIDTH//2 - msg.get_width()//2, 220))
        SCREEN.blit(msg1,(WIDTH//2 - msg.get_width()//2, 260))
        SCREEN.blit(start,(WIDTH//2 - start.get_width()//2, 300))
        pygame.displat.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN  and e.key == pygame.K_RETURN:
                return
    
def game_over_screen():
    while True:
        SCREEN.fill((50, 0 , 0))
        title = BIG_FONT.render('GAMER OVER', True, RED)
        msg = FONT.render("Presiona R para reiniciar", True, WHITE)

        SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 180))
        SCREEN.blit(msg, (WIDTH//2 - msg.get_width()//2, 260))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN  and e.key == pygame.k_r:
                return
    
def victory_screen():
    while True:
        SCREEN.fill(GREEN)
        title = BIG_FOND.render("Felicitaciones",True, WHITE)
        msg = FONT.render("Juego Completado", True, WHITE)
        opt = FONT.render("Enter para reiniciar / ESC para salir", True, WHITE)

        SCREEN.blit(title,(WIDTH//2 - title.get_width()//2, 190))
        SCREEN.blit(msg,(WIDTH//2 - msg.get_width()//2, 250))
        SCREEN.blit(opt(WIDTH//2 - opt.get_width()//2, 300))
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit();sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    main()
                    return
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

#clases
class Player:
    def _init_(self):
        self.x = 100
        self.y = GROUND_Y - 60
        self.vel = 5
        self.vel_y = 0
        self.on_ground = True
        self.lives = 3
        self.rect = PLAYER_IMG.get_rect(topleft=(self.x, self.y))

    def move(self, keys):
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.vel

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -18
            self.on_ground = False
            if JUMP_SOUND:
                JUMP_SOUND.play()

    def apply_gravity(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y

        if self.y >= GROUND_Y -60:
            self.y = GROUND_Y - 60
            self.on_ground = True
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        SCREEN.blit(PLAYER_IMG, (self.x,self.y))

class Enemy:
    def __init__(self, world_x):
        self.world_x = world_x
        self.y = GROUND_Y - 50 
        self.vel = 2
        self.rect = ENEMY_IMG.get_rect()
    
    def update(self):
        self,world_x -= self.vel

    def draw(self, scroll_x):
        self.rect.topleft = (self.world_x - scroll_x self.y)
        SCREEN.blit(ENEMY_IMG, self. rect)

class Coin:
    def __init__(self,worl_x):
        self.world_x = world_x
        self.y = random.randint(260, 340)
        self.rect = COIN_IMG.get.rect()
        
    def draw(self,scroll_x):
        self.rect.topleft = (self.world_x - scroll_x, self.y)
        SCREEN.blit(COIN_IMG,self. rect)

class Goal:
    def __init__(self, world_x):
        self.world_x = world_x
        self.y = GROUND_Y -70
        self.rect = GOAL_IMG.get_rect()

    def draw(self, scroll_x):
        self.rect.topleft = (self.world_x - scroll_x, self.y)
        SCREEN.blit(GOAL_IMG, self.rect)

#juego principal
def main():
    play_background_music()
    start_screen()

    level = 1
    lives = 3
    coins_collectef = 0

    while level <= MAX_LEVELS:
        play = Player()
        player.lives = lives
        enemies = []
        coins = []
        scroll_x = 0
        enemy_spawn_timer = 0

        level_length = 2200 + level * 800
        goal = Goal(level_length)

        for i in range(6+ level):
            coins.append(Coin(400 + i * 300))

        bg = BG_IMAGES[level -1]

        running = True

        while running:
            CLOCK.tick(FPS)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                
            keys = pygame.key.get_pressed()
            player.move(keys)
            player.apply_gravity()

            if player.x > WIDTH//2:
                scroll_x += player.vel
                player.x = WIDTH //2

            SCREEN.fill(BACK)

            bg_x = (-scroll_x * 0.3) % WIDTH
            SCREEN.blit(bg,(bg_x -WIDTH, 0))
            SCREEN.blit(bg,(bg_x, 0))

            enemy_spawn_timer += 1
            if enemy_spawn_timer > 120:
                enemies.append(Enemy(scroll_x + WIDTH + 100))
                enemy_spawn_timer = 0

            player.draw()

            hud = FONT.render(
                f"Nivel:{level}/{MAX_LEVELS} Vidas :{player-lives} Monedas: {coins_collectef}",
                True, WHITE
            )
            SCREEN.blit(hud, (10, 10))

            pygame.display.update()
    victory_screen()
main()

                

    
       


