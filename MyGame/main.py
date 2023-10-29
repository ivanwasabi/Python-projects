import random
import os

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont('Verdana', 20)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0 ,255)
COLOR_RED = (255, 0, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('/Users/ivan/Desktop/Python/MyGame/background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 2

IMAGE_PATH = "/Users/ivan/Desktop/Python/MyGame/Goose"
PLAYER_IMAGES = [pygame.image.load(IMAGE_PATH + '/' + file).convert_alpha() for file in os.listdir(IMAGE_PATH) if file.endswith('.png')]

print(PLAYER_IMAGES)

player_size = (20, 20)
player = pygame.image.load('/Users/ivan/Desktop/Python/MyGame/player.png').convert_alpha()
player_rect = pygame.Rect(0, HEIGHT//2, *player_size)
player_move_down = [0, 4]
player_move_right = [4, 0]
player_move_left = [-4, 0]
player_move_up = [0, -4]

def create_enemy():
    enemy_size = (30, 30)
    #enemy = pygame.image.load('enemy.png').convert_alpha()
    enemy = pygame.transform.scale(pygame.image.load('/Users/ivan/Desktop/Python/MyGame/enemy.png'), (350, 80))
    enemy_rect = pygame.Rect(WIDTH , random.randint(0, HEIGHT - enemy_size[1]), *enemy_size)
    enemy_move = [random.randint(-8, -6), 0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus_size = (30, 30)
    bonus = pygame.transform.scale(pygame.image.load('/Users/ivan/Desktop/Python/MyGame/bonus.png'), (150, 200))
    #bonus = pygame.image.load('bonus.png').convert_alpha()
    bonus_rect = pygame.Rect(random.randint(0, WIDTH - bonus_size[0]), 0, *bonus_size)
    bonus_move = [0, random.randint(1, 4)]
    return [bonus, bonus_rect, bonus_move]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT +2
pygame.time.set_timer(CREATE_BONUS, 1500)

CHANGE_IMAGE = pygame.USEREVENT +3
pygame.time.set_timer(CHANGE_IMAGE, 200)

enemies = []
bonuses = []

score = 0

image_index = 0

game_over_font = pygame.font.Font(None, 36)
game_over_text1 = game_over_font.render("Game Over", True, (0, 0, 0))
game_over_text2 = game_over_font.render("Press Q for Quit", True, (0, 0, 0))

playing = True

while playing:
    FPS.tick(120)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            image_index += 1
            if image_index == len(PLAYER_IMAGES):
                image_index = 0
            player = PLAYER_IMAGES[image_index]
            
    
    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1,0))
    main_display.blit(bg, (bg_X2,0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)
    
    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
                main_display.blit(game_over_text1, (WIDTH // 2 - game_over_text1.get_width() // 2, HEIGHT // 2 - game_over_text1.get_height()))
                main_display.blit(game_over_text2, (WIDTH // 2 - game_over_text2.get_width() // 2, HEIGHT // 2))

                pygame.display.update()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                pygame.quit()
                                quit()
                playing = False


    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))
    main_display.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left <0:
            enemies.pop(enemies.index(enemy))


    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT:
            bonuses.pop(bonuses.index(bonus))