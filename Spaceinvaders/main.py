import pygame
from pygame import mixer
import random
import math

# Intalize pygame
pygame.init()

# Create screen
screenWidth = 800
screenHeight = 600

flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.SCALED
screen = pygame.display.set_mode((screenWidth, screenHeight), flags)

# Backround
bg = pygame.image.load("backround.png").convert()


# Backround Sound
mixer.music.load("bgmusic.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("icon.png").convert_alpha()
pygame.display.set_icon(icon)

# Player
playerimg = pygame.image.load("spaceship.png").convert_alpha()
playerX = 370
playerY = 480
playerX_change = 0
playerSpeed = 4

# Enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyJumpDistance = []
number_of_enemies = 6

for i in range(number_of_enemies):
    enemyimg.append(pygame.image.load("alien.png").convert_alpha())
    enemyX.append(random.randint(0, screenWidth - enemyimg[i].get_width()))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(6)
    enemyJumpDistance.append(25)

# Bullet
bulletimg = pygame.image.load("bullet.png").convert_alpha()
bulletX = 0
bulletY = playerY
bulletY_change = 10
bullet_state = "ready"  # Ready state is when the bullet is hidden and Fire state is when its moving
bullet_start = 0

# Score
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
gameoverfont = pygame.font.Font("freesansbold.ttf", 64)

textX = 10
textY = 10


def show_score(x, y):
    shown_score = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(shown_score, (x, y))


def gameover():
    gameover_text = gameoverfont.render("GAME OVER", True, (255, 36, 36))
    screen.blit(gameover_text, (200, 250))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire(x, y):
    global bullet_state
    global bullet_start
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))
    bullet_start = x


# Main game loop
clock = pygame.time.Clock()
run = True
while run:
    clock.tick(60)

    # Creates backround
    screen.fill((50, 50, 50))
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Check for left or right keystroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                playerX_change = -playerSpeed
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerX_change = playerSpeed
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    fire(playerX, bulletY)
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()

        if event.type == pygame.KEYUP:
            if playerX_change < 0:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    playerX_change = 0
            if playerX_change > 0:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    playerX_change = 0

    # Moves player depending on keystrokes
    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    if playerX > screenWidth - playerimg.get_width():
        playerX = screenWidth - playerimg.get_width()

    # Going through each enemy
    for i in range(number_of_enemies):
        # gameover
        if enemyY[i] > 1000:
            gameover()

        # Enemy power increaser
        if score >= 20 and score < 35 and enemyJumpDistance[i] == 25:
            enemyJumpDistance[i] = 35
        if score >= 35 and score < 50 and enemyJumpDistance == 35:
            enemyJumpDistance[i] = 40
            enemyX_change[i] = 8
        if score >= 50 and score < 60 and enemyJumpDistance == 40:
            enemyJumpDistance[i] = 60
            enemyX_change[i] = 10
        if score >= 60 and score < 100 and enemyJumpDistance == 60:
            enemyJumpDistance[i] = 80
            enemyX_change[i] = 12
        if score >= 80 and enemyJumpDistance == 80:
            enemyJumpDistance = 100
            enemyX_change = 16

        # Enemy movement
        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = enemyX_change[i] * -1
            enemyY[i] += enemyJumpDistance[i]
        if enemyX[i] > screenWidth - enemyimg[i].get_width():
            enemyX_change[i] = enemyX_change[i] * -1
            enemyY[i] += enemyJumpDistance[i]

        # Game over detector
        d = math.sqrt(pow(enemyX[i] - playerX, 2) + pow(enemyY[i] - playerY, 2))
        if d < enemyimg[i].get_width():
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            gameover()
            break

        # Bullet collision
        if bulletY > enemyY[i] - bulletimg.get_height() and bulletY < enemyY[i]:
            if (
                bulletX > enemyX[i] - (bulletimg.get_width() - 1)
                and bulletX < enemyX[i] + enemyimg[i].get_width()
            ):
                bulletY = -20
                score += 1
                enemyX[i] = random.randint(0, screenWidth - enemyimg[i].get_width())
                enemyY[i] = random.randint(50, 150)
                death_sound = mixer.Sound("explosion.wav")
                death_sound.play()

                # Enemy increaser
                if score == 20:
                    number_of_enemies += 1
                    enemyimg.append(pygame.image.load("alien.png").convert_alpha())
                    enemyX.append(
                        random.randint(0, screenWidth - enemyimg[i].get_width())
                    )
                    enemyY.append(random.randint(50, 150))
                    enemyX_change.append(4)
                    enemyJumpDistance.append(25)
                if score == 35:
                    number_of_enemies += 1
                    enemyimg.append(pygame.image.load("alien.png").convert_alpha())
                    enemyX.append(
                        random.randint(0, screenWidth - enemyimg[i].get_width())
                    )
                    enemyY.append(random.randint(50, 150))
                    enemyX_change.append(4)
                    enemyJumpDistance.append(25)
                if score == 50:
                    number_of_enemies += 1
                    enemyimg.append(pygame.image.load("alien.png").convert_alpha())
                    enemyX.append(
                        random.randint(0, screenWidth - enemyimg[i].get_width())
                    )
                    enemyY.append(random.randint(50, 150))
                    enemyX_change.append(4)
                    enemyJumpDistance.append(25)
                if score == 60:
                    number_of_enemies += 2
                    enemyimg.append(pygame.image.load("alien.png").convert_alpha())
                    enemyX.append(
                        random.randint(0, screenWidth - enemyimg[i].get_width())
                    )
                    enemyY.append(random.randint(50, 150))
                    enemyX_change.append(4)
                    enemyJumpDistance.append(25)
                    enemyimg.append(pygame.image.load("alien.png").convert_alpha())
                    enemyX.append(
                        random.randint(0, screenWidth - enemyimg[i].get_width())
                    )
                    enemyY.append(random.randint(50, 150))
                    enemyX_change.append(4)
                    enemyJumpDistance.append(25)
                if score == 80:
                    number_of_enemies += 2
                    enemyimg.append(pygame.image.load("alien.png").convert_alpha())
                    enemyX.append(
                        random.randint(0, screenWidth - enemyimg[i].get_width())
                    )
                    enemyY.append(random.randint(50, 150))
                    enemyX_change.append(4)
                    enemyJumpDistance.append(25)
                    enemyimg.append(pygame.image.load("alien.png").convert_alpha())
                    enemyX.append(
                        random.randint(0, screenWidth - enemyimg[i].get_width())
                    )
                    enemyY.append(random.randint(50, 150))
                    enemyX_change.append(4)
                    enemyJumpDistance.append(25)

                print(score)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bullet_state == "fire":
        fire(bullet_start, bulletY)
        bulletY -= bulletY_change

    if bulletY <= -10:
        bulletX = playerX
        bulletY = playerY
        bullet_state = "ready"

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.flip()
