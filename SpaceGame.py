import pygame, math, random
from pygame import mixer

pygame.init()

# CREATE THE SCREEN
screen = pygame.display.set_mode((1100,800))
running = True

# SETTING THE TITLE FOR SPACE GAME
pygame.display.set_caption('MY SPACE GAME')

# MUSIC
mixer.music.load('assets/background.wav')
mixer.music.play(-1)

# SETTING THE ICON FOR THE WINDOW
icon = pygame.image.load('assets/ufo.png')
pygame.display.set_icon(icon)

bg = pygame.image.load('assets/space_background.jpg')

# SETTING UP THE SPACE CRAFT
playerImage = pygame.image.load('assets/space_craft.png')
playerX = 450
playerY = 620
playerChange = 0    
def player(x, y):
    screen.blit(playerImage, (x, y))

# SETTING UP OF EMEMY
enemyImage = []
enemyX = []
enemyY = []
enemyChangeX = []
enemyChangeY = []
numberOfEnemies = 7
for i in range(numberOfEnemies):
    enemyImage.append(pygame.image.load('assets/enemy.png'))
    enemyX.append(random.randint(0, 800))
    enemyY = [100, 150, 200, 150, 250, 300, 350]
    enemyChangeX.append(2.5)
    enemyChangeY.append(70)
def enemy(x, y, i):
    screen.blit(enemyImage[i], (x, y))

# SETTING UP THE BULLET
bulletImage = pygame.image.load('assets/bullet.png')
bulletX = 450
bulletY = 650
bulletChangeX = 0
bulletChangeY = 7
bulletState = 'ready'
def fireBullets(x, y):
    global bulletState
    bulletState = 'fire'
    screen.blit(bulletImage, (x + 50, y))

# COLLISION
def isCollision(enemyX, enemyY, bulletX, bulletY):  
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 100:
        return True
    else:
        return False

# GAME OVER
def gameOver():
    overFont = pygame.font.Font('assets/FreeSans/FreeSansBold.ttf', 64)
    overFontScore = pygame.font.Font('assets/FreeSans/FreeSansBold.ttf', 55)
    overText = overFont.render('GAME OVER', True, (255, 255, 255))
    overTextScore = overFontScore.render('SCORE : ' + str(scoreValue), True, (255, 255, 255))
    screen.blit(overText, (360, 250))
    screen.blit(overTextScore, (410, 320))

# SCORES
scoreValue = 0
font = pygame.font.Font('assets/FreeSans/FreeSansBold.ttf',32)
textX = 10
textY = 10
def score(x, y):
    score = font.render('SCORE : ' + str(scoreValue), True, (255, 255, 255))
    screen.blit(score, (x, y))

titleFont = pygame.font.Font('assets/FreeSans/FreeSansBold.ttf',32)
gameTitle = titleFont.render('SPACE GAME', True, (255, 255, 255))

# INFINITE LOOP TO STOP THE WINDOW ON SCREEN
while running:
    # screen.fill((193, 118, 171)) 
    screen.blit(bg, (0, 0))     # HERE BILT MEANS DRAW
    screen.blit(gameTitle, (850, 10))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # KEYBOARD EVENTS
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerChange = -2
            elif event.key == pygame.K_RIGHT:
                playerChange = 2
            elif event.key == pygame.K_SPACE:
                if bulletState == 'ready':
                    bulletSound = mixer.Sound('assets/laser.wav')
                    bulletSound.play()
                    bulletX = playerX
                    fireBullets(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerChange = 0

    # PLAYER MOVEMENT            
    playerX += playerChange
    if playerX <= 30:
        playerX = 30
    if playerX >= 920:
        playerX = 920    
    player(playerX, playerY)

    # ENEMY MOVEMENT
    for i in range(numberOfEnemies):
        if enemyY[i] >= 560:
            for j in range(numberOfEnemies):
                enemyY[j] = 2000
            gameOver()
            break
        enemyX[i] += enemyChangeX[i]
        if enemyX[i] <= 20:
            enemyX[i] = 20
            enemyChangeX[i] = 2.5
            enemyY[i] += enemyChangeY[i]
        elif enemyX[i] >= 950:
            enemyX[i] = 950
            enemyChangeX[i] = -2.5
            enemyY[i] += enemyChangeY[i]

        # COLLISION
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)        
        if collision:
            explosionSound = mixer.Sound('assets/explosion.wav')
            explosionSound.play()
            explosionImage = pygame.image.load('assets/explosion.png')
            scoreValue += 1
            screen.blit(explosionImage, (enemyX[i], enemyY[i]))
            bulletState = 'ready'
            bulletY = 650
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = 100
        enemy(enemyX[i], enemyY[i], i)

    # BULLET MOVEMENT
    if bulletY<= 0:
        bulletY = 650
        bulletState = 'ready'
    if bulletState == 'fire':
        bulletY -= bulletChangeY
        fireBullets(bulletX, bulletY)
    score(textX, textY)
    pygame.display.update() # AFTER EVERY CHANGE WE NEED TO UPDATE THE DISPLAY
