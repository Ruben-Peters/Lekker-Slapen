import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
blue = (0,0,255)
bright_red = (255,0,0)
bright_green = (0,255,0)

block_color = (53,115,255)

car_width = 80

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('League of Slapen')
clock = pygame.time.Clock()

carImg = pygame.image.load('teemo4.png')

thingImg = pygame.image.load('minion.png')

background = pygame.image.load('background.png')

bulletImg = pygame.image.load('bullet.png')

def car(x,y):
    gameDisplay.blit(carImg, (x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def message_crash(text):
    largeText = pygame.font.Font('freesansbold.ttf',100)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)
    game_intro()

def crash():
    message_crash('Lekker Slapen')

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def quitgame():
    pygame.quit()
    quit()

########################################################
## Specific enemy for SLAPEN Game
def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: "+str(count), True, white)
    gameDisplay.blit(text,(0,0))

def things(thingx, thingy, thingw, thingh, color):
    gameDisplay.blit(thingImg, (thingx,thingy))


########################################################
## ENEMY for WINTERSLAAP Game
enemyImg = thingImg

def enemy(enemy_X, enemy_Y):
    gameDisplay.blit(enemyImg, (enemy_X, enemy_Y))

#def fire_bullet(x,y)

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        gameDisplay.fill(black)
        largeText = pygame.font.Font('freesansbold.ttf', 90)
        TextSurf, TextRect = text_objects("League of Slapen", largeText)
        TextRect.center = ((display_width/2), ((display_height/2)-100))
        gameDisplay.blit(TextSurf, TextRect)
        
        button("Slapen", ((display_width/2) - 75),320,150,50, green,bright_green, game_loop)
        button("Winterslaap", ((display_width/2) - 75),400,150,50, green,bright_green, game_loop2)
        button("Quit", ((display_width/2) - 75),500,150,50, red,bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)

def game_loop():

    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0

    ## ENEMY voor Slapen
    thing_starty = -500
    thing_speed = 4
    thing_width = 100
    thing_height = 80    
    thing_startx = random.randrange(0, (display_width - thing_width))

    dodged = 0 

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0


        x += x_change

        gameDisplay.fill(white)

        gameDisplay.blit(background,(0,0))

        things(thing_startx, thing_starty, thing_width, thing_height, black)
        
        thing_starty += thing_speed    
        car(x,y)
        things_dodged(dodged)

        if x  >= (display_width - car_width):
            x = (display_width - car_width)
        if x <= 0:
            x = 0

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, (display_width - thing_width))
            dodged += 1
            thing_speed += 1
            #thing_width += (dodged *1.1)

        if y < thing_starty+thing_height:
            #print('y crossover')

            if x > thing_startx and x < thing_startx + thing_width or x+car_width > thing_startx and x + car_width < thing_startx+thing_width:
                #print('x crossover')
                crash()


        pygame.display.update()
        clock.tick(60)


def game_loop2():
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0

    ## Enemy parameters
    enemy_width = 100
    enemy_height = 80   
    enemy_X = random.randint(0, display_width)
    enemy_Y = random.randint(10, 120)
    enemy_X_change = 2
    enemy_Y_change = 40

    ## Bullet 
    # ready state: it is not shown
    # fire state: bullet is currently moving
    bullet_X = 0
    bullet_Y = (display_height * 0.8)
    bullet_Y_change = 40
    bullet_state = "ready"

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
       
        gameDisplay.fill(white)

        gameDisplay.blit(background,(0,0))

        enemy_X += enemy_X_change

        car(x,y)
        enemy(enemy_X, enemy_Y)

        #making sure Teemo does not go out of the boundaries
        x += x_change

        if x  >= (display_width - car_width):
            x = (display_width - car_width)
        if x <= 0:
            x = 0
        
        #Minions movement
        if enemy_X  <= 0:
            enemy_X_change = 2
            enemy_Y += enemy_Y_change
        if enemy_X >= (display_width - enemy_width):
            enemy_X_change = -2
            enemy_Y += enemy_Y_change



        pygame.display.update()
        clock.tick(60)

game_intro()