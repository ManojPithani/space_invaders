import pygame
import random
import math
from pygame import mixer

# display screen
pygame.init()
screen = pygame.display.set_mode((800, 600))

# set caption and add logo
icon = pygame.image.load('rocket.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('SPACE INVADER')

# back ground attributes
background = pygame.image.load('background1.jpg')
mixer.music.load('background (1).wav')
mixer.music.play(-1)

# score displaying
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# gameover text
gameover_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score_val = font.render("score:" + str(score), True, (255, 255, 255))
    screen.blit(score_val, (x, y))


def game_over_text():
    gameover_text = gameover_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(gameover_text, (200, 250))


playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 500
playerX_changed = 0

enemyImg = []
enemyX = []
enemyY = []
enemyY_changed = []
enemyX_changed = []
num_of_enemies = 10

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(40, 150))
    enemyX_changed.append(0.8)
    enemyY_changed.append(40)

bulletImg = pygame.image.load('bullet.png')
bulletX = 370
bulletY = 500
bulletX_changed = 0
bulletY_changed = 1
bullet_state = "ready"


# function to draw or move the player
def player(x, y):
    screen.blit(playerImg, (x, y))


# function to draw or move the player
def enemy(x, y):
    screen.blit(enemyImg[i], (x, y))


# function to draw and move the bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# to make sure display screen stays until closed
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keystroke press check
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_changed = -0.6
            if event.key == pygame.K_RIGHT:
                playerX_changed = 0.6
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_changed = 0

    # screen background color
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    playerX += playerX_changed
    # player movement
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    playerX += playerX_changed

    # enemy movement
    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_changed[i]
        if enemyX[i] <= 0:
            enemyX_changed[i] = 0.5
            enemyY[i] += 40
        elif enemyX[i] >= 736:
            enemyX_changed[i] = -0.5
            enemyY[i] += 40

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 500
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(40, 150)

        enemy(enemyX[i], enemyY[i])

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_changed

    if bulletY <= 0:
        bulletY = 500
        bullet_state = "ready"

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
