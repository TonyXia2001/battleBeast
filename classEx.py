'''
World of War Tanks - Battle Beasts
Team members: Alex, Tony, Samyar, Braden, Sangar
05/22/2018
Game description:
Press WASD to move the tank. Press the space bar to fire bullets. The targets
appear randomly on the map.
'''
# importing modules
import pygame
import random

'''
GLOBAL VARIABLES//GLOBAL VARIABLES//GLOBAL VARIABLES//GLOBAL VARIABLES//GLOBAL VARIABLES//GLOBAL VARIABLES
'''
# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# images of sprites
SPRITES = {"left": "Player_Image_Left.png",
           "right": "Player_Image_Right.png",
           "up": "Player_Image_Up.png",
           "down": "Player_Image_Down.png"}
BULLET = {"left": "Bullet_Left.png",
          "right": "Bullet_Right.png",
          "up": "Bullet_Up.png",
          "down": "Bullet_Down.png"}
TARGET = "TargetSprite.png"
MAP = "map.png"
WELCOME = "Titlepage.png"
WELCOME_1 = "Titlepage_Clear.png"

# screen settings
SCREEN_W = 700
SCREEN_H = 800

#BGM
MUSIC_RARE = "MansNotHot.mp3"
MUSIC_COMMON = "Sabaton-Panzerkampf.mp3"

'''
MAIN PROGRAM//MAIN PROGRAM//MAIN PROGRAM//MAIN PROGRAM//MAIN PROGRAM//MAIN PROGRAM//MAIN PROGRAM//MAIN PROGRAM
'''
def main():

    # initiating pygame
    pygame.init()
    musicRandom = random.randint(0, 99)
    if musicRandom == 4:
        pygame.mixer.music.load(MUSIC_RARE)
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.load(MUSIC_COMMON)
        pygame.mixer.music.play(-1)

    # setting up the display window
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("World of Wartanks - Battle Beasts")
    windowIcon = pygame.image.load(SPRITES["down"])
    pygame.display.set_icon(windowIcon)
    # clock
    clock = pygame.time.Clock()
    welcomePage = True
    running = True
    scoreboard = True
    endLoop = True

    '''
    WELCOME LOOP//WELCOME LOOP//WELCOME LOOP//WELCOME LOOP//WELCOME LOOP//WELCOME LOOP//WELCOME LOOP//WELCOME LOOP
    '''

    starttime = 0
    start_minus = 0
    start_change_con = -1

    welcomeFont = pygame.font.SysFont('Calibri', 25, True, False)  # import font
    welcomeScreen = pygame.image.load(WELCOME)
    welcomeScreen_2 = pygame.image.load(WELCOME_1)

    screen.blit(welcomeScreen, (0, 0))
    while welcomePage:
        # quit the game when the red cross is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                welcomePage = False
                running = False
                endLoop = False
                break
        starttime = pygame.time.get_ticks() - start_minus
        if starttime >= 1000:
            start_change_con *= -1
            start_minus = pygame.time.get_ticks()
        if start_change_con == -1:
            screen.fill(WHITE)
            screen.blit(welcomeScreen, (0, 0))
        else:
            screen.fill(WHITE)
            screen.blit(welcomeScreen_2, (0, 0))
        # Key bindings
        welcomeKeys = pygame.key.get_pressed()
        if welcomeKeys[pygame.K_SPACE]:
            welcomePage = False

        pygame.display.flip()
        # framerate
        clock.tick(20)

    pygame.time.delay(250)

    '''
    MAIN LOOP//MAIN LOOP//MAIN LOOP//MAIN LOOP//MAIN LOOP//MAIN LOOP//MAIN LOOP//MAIN LOOP//MAIN LOOP//MAIN LOOP
    '''
    # setting up the map
    map = pygame.image.load(MAP)
    map_rect = map.get_rect()
    # setting up the objects
    target1 = Target(random.randint(6, 700 - 6), random.randint(6, 700 - 6))
    tank1 = Tank(3, 40, 80, map)
    # setting up a master class that controls everything
    gamehost1 = GameHost(tank1, target1)
    # setting up the text display
    consistentFont = pygame.font.SysFont('Calibri', 25, True, False)  # import font
    scoreText = consistentFont.render("Score: " + str(gamehost1.score), True, BLACK)
    accText = consistentFont.render("Accuracy: N/A", True, BLACK)
    exitFont = consistentFont.render("Press 'ESC' to exit.", True, BLACK)

    timeStart = pygame.time.get_ticks()

    while running:
        # quit the game when the red cross is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                endLoop = False
                break
        # check for game end condition
        if gamehost1.score == 25:
            timeEnd = pygame.time.get_ticks()
            break


        # Key bindings
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            tank1.move("up")
        elif keys[pygame.K_a]:
            tank1.move("left")
        elif keys[pygame.K_s]:
            tank1.move("down")
        elif keys[pygame.K_d]:
            tank1.move("right")
        if keys[pygame.K_SPACE]:
            tank1.fire()
        if keys[pygame.K_ESCAPE]:
            running = False
            scoreboard = False
            break

        # check for the collision between bullets and target
        gamehost1.collisiondetect()
        # if the target is hit
        if target1.isHit == True:
            # create a new target object
            target1 = Target(random.randint(6, 677), random.randint(6, 677))
            # inform the master about the new target
            gamehost1.target = target1
            # refresh the score/accuracy count
            scoreText = consistentFont.render("Score: " + str(gamehost1.score),
                                         True, BLACK)
            accText = consistentFont.render("Accuracy: " +
                                       str(round(gamehost1.score / tank1.shotsFired * 100, 1)) +
                                       "%", True, BLACK)

        # refresh the screen
        screen.fill(WHITE)
        # stick everything onto the screen
        screen.blit(map, map_rect)
        screen.blit(tank1.image, tank1.imageBox)
        # only if tank1 has fired, do we try to put the bullets onto the screen
        if tank1.fired:
            for i in range(0, len(tank1.bullet)):
                validMove = tank1.bullet[i].move(tank1.bullet[i].direction)
                screen.blit(tank1.bullet[i].sprite, tank1.bullet[i].imageBox)
                # if the bullet moves out of the screen, refer to the bullet class
                # definition of move method
                if validMove == -1:
                    tank1.bullet[i] = -1      # set the bullet to -1 for now
                    # refresh the accuracy/score count
                    accText = consistentFont.render(
                        "Accuracy: " + str(round(gamehost1.score / tank1.shotsFired * 100, 1)) + "%",
                        True, BLACK)
            while True:
                try:
                    tank1.bullet.remove(-1)  # remove everything item that's -1
                except ValueError:
                    break
        screen.blit(target1.image, target1.imageBox)
        screen.blit(scoreText, [10, 700])
        screen.blit(accText, [200, 700])
        screen.blit(exitFont, [50, 750])
        time = round((pygame.time.get_ticks() - timeStart)/1000, 1)
        screen.blit(consistentFont.render("Time: " + str(time), True, BLACK), [500, 700])
        # update the page
        pygame.display.flip()
        # framerate
        clock.tick(60)

    '''
    END PAGE//END PAGE//END PAGE//END PAGE//END PAGE//END PAGE//END PAGE//END PAGE//END PAGE//END PAGE//END PAGE
    '''
    if scoreboard == True:
        if tank1.shotsFired != 0:
            scoreText = consistentFont.render("Score: " + str(int(round(gamehost1.score ** 2 / tank1.shotsFired * 100/time, 2) * 10)), True, BLACK)
        else:
            scoreText = consistentFont.render("Score: N/A", True, BLACK)
        while endLoop:
            # quit the game when the red cross is pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    endLoop = False
                    break

            screen.fill(WHITE)
            screen.blit(scoreText, [50, 350])
            screen.blit(accText, [300, 350])
            screen.blit(consistentFont.render("Time: " + str(time), True, BLACK), [550, 350])
            # update the page
            pygame.display.flip()
            # framerate
            clock.tick(60)
        # quit pygame
        pygame.quit()
'''
START OF TANK CLASS//START OF TANK CLASS//START OF TANK CLASS//START OF TANK CLASS//START OF TANK CLASS
START OF TANK CLASS//START OF TANK CLASS//START OF TANK CLASS//START OF TANK CLASS//START OF TANK CLASS
START OF TANK CLASS//START OF TANK CLASS//START OF TANK CLASS//START OF TANK CLASS//START OF TANK CLASS
'''
class Tank(object):
    '''
    Tank class
    constructor:
        tankObj1 = tank(speed, xPosition, yPosition, map)
            speed: integer, the velocity of the tank, should always be smaller than the thickness of the wall
            xPosition: integer, the spawning x value of the top left corner of the sprite
            yPosition: integer, the spawning y value of the top left corner of the sprite
            map: pygame.surface object, the map on which the tank is displayed
    instance methods:
        tankObj1.move(direction)
            direction: string, the direction of the movement. can only be either
                "left", "right", "up", or "down".
        tankObj1.fire()
            fire a bullet at the direction at which the tank is facing
    instance variables:
        speed: int, speed of the tank class instance
        xpos, ypos: int, the position of the tank class instance
        image, imageBox: pygame.surface and pygame.rect objects.
        fired: boolean, has the tank fired any shot?
        bullet: a list of bullets fired but yet expired
        lastTimeFiring: int, last time firing a bullet, in ms
        shotsFired: int, shots fired in total
    '''
    # constructor
    def __init__(self, speed, posX, posY, map):
        self.speed = speed
        self.xpos = posX
        self.ypos = posY
        self.image = pygame.image.load(SPRITES["up"])
        self.imageBox = self.image.get_rect(x=posX, y=posY)
        self.direction = "up"
        self.fired = False
        self.bullet = []
        self.LastTimeFiring = -1000
        self.shotsFired = 0
        self.mapSurface = map

    def move(self, direction):
        if direction == "left":
            self.xpos -= self.speed
            # if the runs over a wall, move back
            for i in range(0, 25, 6):   # checking the front-most row of pixels
                for j in range(0, 6, 5):
                    if self.mapSurface.get_at((self.xpos + j, self.ypos + i)) == (0, 0, 0, 255):
                        self.xpos += self.speed
                        return
            # refresh the sprite image
            self.image = pygame.image.load(SPRITES["left"])
            # move the sprite hitbox
            self.imageBox = self.image.get_rect(x = self.xpos, y = self.ypos)
            self.direction = "left"
        elif direction == "right":
            self.xpos += self.speed
            for i in range(0, 25, 6):
                for j in range(0, 6, 5):
                    if self.mapSurface.get_at((self.xpos + 30 - j, self.ypos + i)) == (0, 0, 0, 255):
                        self.xpos -= self.speed
                        return
            self.image = pygame.image.load(SPRITES["right"])
            self.imageBox = self.image.get_rect(x = self.xpos, y = self.ypos)
            self.direction = "right"
        elif direction == "up":
            self.ypos -= self.speed
            for i in range(0, 25, 6):
                for j in range(0, 6, 5):
                    if self.mapSurface.get_at((self.xpos + i, self.ypos + j)) == (0, 0, 0, 255):
                        self.ypos += self.speed
                        return
            self.image = pygame.image.load(SPRITES["up"])
            self.imageBox = self.image.get_rect(x = self.xpos, y = self.ypos)
            self.direction = "up"
        elif direction == "down":
            self.ypos += self.speed
            for i in range(0, 25, 6):
                for j in range(0, 6, 5):
                    if self.mapSurface.get_at((self.xpos + i, self.ypos + 30-j)) == (0, 0, 0, 255):
                        self.ypos -= self.speed
                        return
            self.image = pygame.image.load(SPRITES["down"])
            self.imageBox = self.image.get_rect(x = self.xpos, y = self.ypos)
            self.direction = "down"

    def fire(self):
        self.fired = True
        # record the current time
        currentTime = pygame.time.get_ticks()
        # compare the current time with the last firing time. only fire when the
        # difference is larger than 1000ms

        if currentTime >= self.LastTimeFiring + 1000:
            # adding the bullet to the bullet list
            self.bullet.append(Bullet(self.xpos, self.ypos, self.direction, self.mapSurface))
            self.LastTimeFiring = currentTime
            self.shotsFired += 1
            # if there are more than 5 bullets, delete the earlier one
            if len(self.bullet) > 5:
                del self.bullet[0]

'''
START OF THE BULLET CLASS//START OF THE BULLET CLASS//START OF THE BULLET CLASS//START OF THE BULLET CLASS
START OF THE BULLET CLASS//START OF THE BULLET CLASS//START OF THE BULLET CLASS//START OF THE BULLET CLASS
START OF THE BULLET CLASS//START OF THE BULLET CLASS//START OF THE BULLET CLASS//START OF THE BULLET CLASS
'''

class Bullet(object):

    def __init__(self, posX, posY, direction, map):
        self.xPos = posX
        self.yPos = posY
        self.speed = 10
        self.direction = direction
        self.mapSurface = map
        self.sprite = pygame.image.load(BULLET[direction])
        if direction == "down":
            self.imageBox = self.sprite.get_rect(x=posX + 9, y=posY + 30)
        if direction == "up":
            self.imageBox = self.sprite.get_rect(x=posX + 9, y=posY - 12)
        if direction == "right":
            self.imageBox = self.sprite.get_rect(x=posX + 30, y=posY + 9)
        if direction == "left" :
            self.imageBox = self.sprite.get_rect(x=posX - 12, y=posY + 9)

    def move(self, direction):

        if (self.yPos > 700 or self.yPos < 0) or (self.xPos > 700 or self.xPos < 0):
            return -1

        if direction == "left":
            self.xPos -= self.speed
            for i in range(9, 18, 4):   # checking the front-most row of pixels
                for j in range(2, 15, 4):
                    try:
                        if self.mapSurface.get_at((self.xPos + j, self.yPos + i)) == (0, 0, 0, 255):
                            return -1
                    except IndexError:
                        return -1
            self.image = pygame.image.load(BULLET["left"])
            self.imageBox.x = self.xPos + 1
            self.imageBox.y = self.yPos + 9
            self.direction = "left"

        elif direction == "right":
            self.xPos += self.speed
            for i in range(9, 18, 4):   # checking the front-most row of pixels
                for j in range(2, 15, 4):
                    try:
                        if self.mapSurface.get_at((self.xPos + 12 - j, self.yPos + i)) == (0, 0, 0, 255):
                            return -1
                    except IndexError:
                        return -1
            self.image = pygame.image.load(BULLET["right"])
            self.imageBox.x = self.xPos + 17
            self.imageBox.y = self.yPos + 9
            self.direction = "right"

        elif direction == "up":
            self.yPos -= self.speed
            for i in range(9, 18, 4):   # checking the front-most row of pixels
                for j in range(2, 15, 4):
                    try:
                        if self.mapSurface.get_at((self.xPos + i, self.yPos + j)) == (0, 0, 0, 255):
                            return -1
                    except IndexError:
                        return -1
            self.image = pygame.image.load(BULLET["up"])
            self.imageBox.x = self.xPos + 9
            self.imageBox.y = self.yPos + 1
            self.direction = "up"

        elif direction == "down":
            self.yPos += self.speed
            for i in range(9, 18, 4):   # checking the front-most row of pixels
                for j in range(2, 15, 4):
                    try:
                        if self.mapSurface.get_at((self.xPos + i, self.yPos + 12 - j)) == (0, 0, 0, 255):
                            return -1
                    except IndexError:
                        return -1
            self.image = pygame.image.load(BULLET["down"])
            self.imageBox.x = self.xPos + 9
            self.imageBox.y = self.yPos + 17
            self.direction = "down"

        return 0


'''
START OF THE TARGET CLASS//START OF THE TARGET CLASS//START OF THE TARGET CLASS//START OF THE TARGET CLASS
START OF THE TARGET CLASS//START OF THE TARGET CLASS//START OF THE TARGET CLASS//START OF THE TARGET CLASS
START OF THE TARGET CLASS//START OF THE TARGET CLASS//START OF THE TARGET CLASS//START OF THE TARGET CLASS
'''

class Target(object):
    '''
    Target class
    constructor syntax:
        targetObj1 = Target(x, y)
            x, y: the position of the tank firing the bullet
    instance variables:
        xPos, yPos: int, the position of the target
        image, imageBox: pygame.image, pygame.Surface
        isHit: whether or not the target has been hit
    '''
    def __init__(self, posX, posY):
        self.yPos = posY
        self.xPos = posX
        self.image = pygame.image.load(TARGET)
        self.imageBox = self.image.get_rect(x=self.xPos, y=self.yPos)
        self.isHit = False

'''
START OF THE GAMEHOST CLASS//START OF THE GAMEHOST CLASS//START OF THE GAMEHOST CLASS//START OF THE GAMEHOST CLASS
START OF THE GAMEHOST CLASS//START OF THE GAMEHOST CLASS//START OF THE GAMEHOST CLASS//START OF THE GAMEHOST CLASS
START OF THE GAMEHOST CLASS//START OF THE GAMEHOST CLASS//START OF THE GAMEHOST CLASS//START OF THE GAMEHOST CLASS
'''

class GameHost(object):
    '''
    GameHost class
    constructor:
    syntax: master = GameHost(tank, target)
    instance variables:
        tank: the tank in the game
        target: the current target
        score: number of shots hit
        shotsFired: number of shots fired in total
    instance method:
        gameHostObj.collisiondetect()
        detects whether any bullet hits the current target
    '''
    def __init__(self, tank, target):
        self.tank = tank
        self.target = target
        self.score = 0
        self.shotsFired = 0

    def collisiondetect(self):
        for i in range(0, len(self.tank.bullet)):
            if self.tank.bullet[i].imageBox.colliderect(self.target.imageBox) == True:
                del self.tank.bullet[i]
                self.target.isHit = True
                self.score += 1
                break

if __name__ == '__main__':
   main()
