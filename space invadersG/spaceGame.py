import pygame
import random
import math
from pygame import mixer

# initialize the py game

pygame.init()



# create a screen
screen = pygame.display.set_mode((800, 600))  # (width,height)

# background image
Background = pygame.image.load("gameBG.png")

#background music
mixer.music.load('background.wav')
mixer.music.play(-1)    #-1 is to loop the sound

# Title
pygame.display.set_caption("SpaceInvaders")
icon = pygame.image.load("startup.png")
pygame.display.set_icon(icon)

# Player
playerimg = pygame.image.load("space-invaders.png")
playerX = 370
playerY = 480
playerX_change = 4
playerY_change = 0

# enemy
enemyimg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
no = 5

for i in range(no):
    enemyimg.append(pygame.image.load("monster.png"))
    enemyX.append(random.randint(0, 700))
    enemyY.append(random.randint(50, 200))
    enemyX_change.append(3)
    enemyY_change.append(45)

# bullet
bulletimg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"  # we can't see the bullet


# Score
score = 0
font= pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10

# Hiscore
with open("hiscore.txt","r") as f:
    hiscore=f.read()


# Game over text
overfont= pygame.font.Font('freesansbold.ttf',70)

def game_over_text():
    over_text = overfont.render("   Game Over", True, (255, 255, 255))
    text = font.render("Your Score : " + str(score), True, (255, 255, 255))
    hitext = font.render("HiScore : " + str(hiscore), True, (255, 255, 255))
    screen.blit(over_text, (100,250))
    screen.blit(text, (250, 350))
    screen.blit(hitext, (300, 400))
def show_score(x,y):
    global score_s
    score_s = font.render("Score : "+ str(score)+"  HiScore : " + str(hiscore),True,(255,255,255))

    screen.blit(score_s, (x, y))

def player(x, y):
    screen.blit(playerimg, (x, y))  # drawing the player


def enemy(x, y,i):
    screen.blit(enemyimg[i], (x, y))  # drawing the player


def fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def isCollision(eX,eY,bX,bY):
    dis = math.sqrt(math.pow((eX - bX),2) + (math.pow((eY - bY),2)))
    if dis <= 30:
        return True
    else:
        return False


# Game loop
running = True
while running:
    # Background color
    screen.fill((5, 29, 52))  # this should be first (working on layers)
    # Background image
    screen.blit(Background, (0, 0))
    for event in pygame.event.get():  # every event tracing
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed then check whether its left r right

        if event.type == pygame.KEYDOWN:  # any key pressed
            # print("keystroke is pressed")


            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound=mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX  # gets the x coordinate of player
                    bulletY = 480
                    fire(bulletX, bulletY)


        if event.type == pygame.KEYUP:  # Key realeased
            print("keystroke is realesed")




    # checking for bounderies
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # image size is 64x64(size consation)
        playerX = 736


    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire(bulletX, bulletY)
        bulletY -= bulletY_change

    # Enemy movement
    for i in range(no):

        # Game over
        if enemyY[i] > 450:
            for j in range(no):
                enemyY[j]=2000
            game_over_text()
            if score > int(hiscore):
                hiscore = score
                with open("hiscore.txt", "w")as f:
                    f.write(str(hiscore))
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i]= 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:  # image size is 64x64(size consation)
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = playerY
            bullet_state = "ready"
            score += 1
            print(score)
            enemyX[i] = random.randint(0, 700)
            enemyY[i]= random.randint(50, 200)
        enemy(enemyX[i], enemyY[i], i)

# Player movement
    playerX += playerX_change  # changing the x and y continuously
    if playerX <= 0:
        playerX_change = 4
        playerX += playerX_change
    elif playerX >= 736:  # image size is 64x64(size consation)
        playerX_change = -4
        playerX += playerX_change

    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()  # you always have to update your display
