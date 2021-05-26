import math
import random

import pygame
from pygame import mixer


def new_game():
    # Initialize the pygame
    pygame.init()

    # create the screen
    screen = pygame.display.set_mode((800, 600))

    # Background
    background = pygame.image.load('img.png')

    # Sound
    mixer.music.load("background.wav")
    mixer.music.play(-1)

    # Caption and Icon
    pygame.display.set_caption("Space Invader")
    icon = pygame.image.load('ufo.png')
    pygame.display.set_icon(icon)

    # Player
    playerImg = pygame.image.load('player.png')
    playerX = 370
    playerY = 480
    playerX_change = 0

    # Enemy
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 6

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('enemy.png'))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(1.5)
        enemyY_change.append(40)

    # Bullet

    # Ready - You can't see the bullet on the screen
    # Fire - The bullet is currently moving

    bulletImg = pygame.image.load('bullet.png')
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 3.5
    bullet_state = "ready"


    # Score

    score_value = 0
    highscore_value = 122
    font = pygame.font.Font('freesansbold.ttf', 32)

    textX = 10
    testY = 10

    # Game Over
    over_font = pygame.font.Font('freesansbold.ttf', 64)

    game_loop(screen, background, playerX, playerImg, playerX_change, playerY, enemyImg, enemyY,
              enemyX, enemyX_change, enemyY_change, num_of_enemies, bulletImg, bulletX, bulletY,
              bulletY_change, bulletX_change, bullet_state, score_value, highscore_value, font,
              textX, testY, over_font)


def show_score(x, y, font, score_value, screen):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def show_highscore(x, y, font, highscore_value, screen):
    highscore = font.render("Highscore : " + str(highscore_value), True, (255, 255, 255))
    screen.blit(highscore, (200, y))


def game_over_text(over_font, screen):
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y, screen, playerImg):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i, screen, enemyImg):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y, screen, bulletImg):
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))
    return bullet_state

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def game_loop(screen, background, playerX, playerImg, playerX_change, playerY, enemyImg, enemyY,
              enemyX, enemyX_change, enemyY_change, num_of_enemies, bulletImg, bulletX, bulletY,
              bulletY_change, bulletX_change, bullet_state, score_value, highscore_value, font,
              textX, testY, over_font):
    # Game Loop
    running = True
    while running:

        # RGB = Red, Green, Blue
        screen.fill((0, 0, 0))
        # Background Image
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if keystroke is pressed check whether its right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -1.8
                if event.key == pygame.K_RIGHT:
                    playerX_change = 1.8
                if event.key == pygame.K_a:
                    score_value += 50
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletSound = mixer.Sound("laser.wav")
                        bulletSound.play()
                        # Get the current x co0rdinate of the spaceship
                        bulletX = playerX
                        bullet_state = fire_bullet(bulletX, bulletY, screen, bulletImg)
                if event.key == pygame.K_r:
                    running = False
                    new_game()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # 5 = 5 - 0.1 = 4.9
        # 5 = 5 + 0.1 = 5.1

        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy Movement
        for i in range(num_of_enemies):

            # Game Over
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text(over_font, screen)
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 1.5
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -1.5
                enemyY[i] += enemyY_change[i]

            if score_value >= 50:
                if enemyX_change[i] == 1.5:
                    enemyX_change[i] += 0.3
                if enemyX_change[i] == -1.5:
                    enemyX_change[i] -= 0.3

            if score_value >= 50:
                if playerX_change == 1.5:
                    playerX_change += 0.3
                if playerX_change == -1.5:
                    playerX_change -= 0.3

            if score_value >= 100:
                if enemyX_change[i] == 1.8:
                    enemyX_change[i] += 0.3
                if enemyX_change[i] == -1.8:
                    enemyX_change[i] -= 0.3

            if score_value >= 100:
                if playerX_change == 1.8:
                    playerX_change += 0.3
                if playerX_change == -1.8:
                    playerX_change -= 0.3

            if score_value >= 150:
                if enemyX_change[i] == 2.1:
                    enemyX_change[i] += 0.3
                if enemyX_change[i] == -2.1:
                    enemyX_change[i] -= 0.3

            if score_value >= 150:
                if playerX_change == 2.1:
                    playerX_change += 0.3
                if playerX_change == -2.1:
                    playerX_change -= 0.3

            if score_value >= 175:
                if enemyX_change[i] == 2.4:
                    enemyX_change[i] += 0.3
                if enemyX_change[i] == -2.4:
                    enemyX_change[i] -= 0.3

            if score_value >= 175:
                if playerX_change == 2.4:
                    playerX_change += 0.3
                if playerX_change == -2.4:
                    playerX_change -= 0.3

            if score_value >= 200:
                if enemyX_change[i] == 2.7:
                    enemyX_change[i] += 0.3
                if enemyX_change[i] == -2.7:
                    enemyX_change[i] -= 0.3

            if score_value >= 200:
                if playerX_change == 2.7:
                    playerX_change += 0.3
                if playerX_change == -2.7:
                    playerX_change -= 0.3

            if score_value >= highscore_value:
                highscore_value = score_value

            # Collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)


            enemy(enemyX[i], enemyY[i], i, screen, enemyImg)

        # Bullet Movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY, screen, bulletImg)
            bulletY -= bulletY_change

        player(playerX, playerY, screen, playerImg)
        show_score(textX, testY, font, score_value, screen)
        show_highscore(textX, testY, font, highscore_value, screen)
        pygame.display.update()

new_game()