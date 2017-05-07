import pygame
from pygame import *
from pygame.locals import *
import math
import os

#Constants
TABLE_HEIGHT = 643
TABLE_WIDTH = 1138
BALL_RADIUS = 35/2

#Function for loading sprite images
def load_image(name,colorkey=None):
    fullname = os.path.join('data/images',name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print('Cannot load image:', name)
        raise SystemExit
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey,RLEACCEL)
    return image,image.get_rect()

#Class to hold all instances of game balls
class Balls():
    def __init__(self):
        self.balls = [Ball('ball_16.png',0)]
        for i in range(1,16):
            ball = Ball('ball_' + str(i) + '.png',i)
            self.balls.append(ball)
    
    #Sets up table to be played
    def reset(self):
        self.balls[0].set_position(3*TABLE_WIDTH/4-27, TABLE_HEIGHT/2)
        self.balls[1].set_position(TABLE_WIDTH/4+27, TABLE_HEIGHT/2)
        self.balls[9].set_position(self.balls[1].rect.x-33,self.balls[1].rect.y-18)
        self.balls[3].set_position(self.balls[1].rect.x-33,self.balls[1].rect.y+18)
        self.balls[4].set_position(self.balls[9].rect.x-33,self.balls[9].rect.y-18)
        self.balls[8].set_position(self.balls[9].rect.x-33,self.balls[9].rect.y+18)
        self.balls[10].set_position(self.balls[3].rect.x-33,self.balls[3].rect.y+18)
        self.balls[11].set_position(self.balls[4].rect.x-33,self.balls[4].rect.y-18)
        self.balls[5].set_position(self.balls[4].rect.x-33,self.balls[4].rect.y+18)
        self.balls[13].set_position(self.balls[8].rect.x-33,self.balls[8].rect.y+18)
        self.balls[6].set_position(self.balls[10].rect.x-33,self.balls[10].rect.y+18)
        self.balls[7].set_position(self.balls[11].rect.x-33,self.balls[11].rect.y-18)
        self.balls[12].set_position(self.balls[11].rect.x-33,self.balls[11].rect.y+18)
        self.balls[2].set_position(self.balls[5].rect.x-33,self.balls[5].rect.y+18)
        self.balls[14].set_position(self.balls[13].rect.x-33,self.balls[13].rect.y+18)
        self.balls[15].set_position(self.balls[6].rect.x-33,self.balls[6].rect.y+18)
    
    def draw(self,surface):
        for ball in self.balls:
            ball.draw(surface)        

    # this is sort of a hack, we could maybe improve this later
    def wallCollisions(self):
        for ball in self.balls:
            x, y = ball.rect.centerx, ball.rect.centery
            if x+BALL_RADIUS >= 1065:
                ball.rect.centerx = 1064 - BALL_RADIUS
                ball.angle = 180-ball.angle
            if x-BALL_RADIUS <= 75:
                ball.rect.centerx += 76 + BALL_RADIUS
                ball.angle = 180-ball.angle
            if y+BALL_RADIUS >=570:
                ball.rect.centery = 569 - BALL_RADIUS
                ball.angle = -ball.angle
            if y-BALL_RADIUS <= 75:
                ball.rect.centery = 76 + BALL_RADIUS
                ball.angle = -ball.angle
            
    # tick in order to have balls move
    def tick(self):
        for ball in self.balls:
            ball.tick()

    def done(self):
        # check if all balls are done moving
        for ball in self.balls:
            if ball.speed != 0:
                return False
        return True
            
#Class for each game ball
class Ball(sprite.Sprite):
    def __init__(self,image,num):
        sprite.Sprite.__init__(self)
        self.image,self.rect = load_image(image,-1)
        self.num = num
        self.speed = 0
        self.angle = 0
        
    def set_position(self,x,y):
        self.rect.x = x
        self.rect.y = y
        
    def draw(self,surface):
        surface.blit(self.image,self.rect)

    def tick(self):
        #print("speed is ", str(self.speed))
        # cos and sin take the angle in radians -- be careful
        self.rect.x += -1 * self.speed * math.cos(self.angle)
        self.rect.y += -1 * self.speed * math.sin(self.angle)
        # use -1 since top left is origin
        if self.speed != 0:
            pass
            #print("decrementing speed")
            #self.speed -= 1
        # gradually get slower
        
#Class for game table        
class Table(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image,self.rect = load_image('table.png')

    def draw(self,surface):
        surface.blit(self.image,self.rect)

'''class Walls():
    def __init__(self):
        self.walls = []
        self.walls.append(Wall(105, 525, 55, 75))     # top left wall
        self.walls.append(Wall(600, 1025, 75, 55))    # top right
        self.walls.append(Wall(1065, 1085, 115, 530)) # right
        self.walls.append(Wall(600, 1025, 570, 590))  # bottom right
        self.walls.append(Wall(110, 525, 570, 590))   # bottom left
        self.walls.append(Wall(55, 75, 115, 530))     # left
        
class Wall():
    def __init__(self, left, right, front): #top, bottom):
        #self.left = left
        #self.right = right
        self.front = front
        self.top = top
        self.bottom = bottom
'''        
#Class for game cue
class Stick(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image,self.rect = load_image('cue.png',-1)
        self.orig_image = self.image
        self.current_x = self.rect.x
        self.curent_y = self.rect.y
        self.power = 0
        self.angle = 0
    
    #Function for drawing back before shot
    def pull(self):
        if self.power == 0:
            self.old_x = self.rect.x
            self.old_y = self.rect.y
        if self.power < 100:    
            self.rect.x += 10
            self.power += 10

    #Function to reset stick to pre-shot position   
    def reset(self):
        self.power = 0
        self.rect.x, self.current_x = self.old_x
        self.rect.y, self.current_y = self.old_y
        
    #Function to release stick before shot
    def release(self):
        if self.power > 0:
            self.rect.x -= 10
            self.power -= 10

    #Function to shoot ball --- TODO: Determine how we want to animate this
    def shoot(self):
        self.rect.x = self.old_x
    
    #Function for setting stick in relation to cue ball
    def set_position(self,x,y):
        self.rect.x = x+BALL_RADIUS
        self.rect.y = y - self.rect.height/2
        
    def draw(self,surface):
        surface.blit(self.image,self.rect)

    # Function to update angle of stick -- follows mouse
    def tick(self, cueball):
        pass
        #curr_x, curr_y = self.rect.x, self.rect.y
        #x, y = pygame.mouse.get_pos()
        #x -= cueball.rect.centerx
        #y -= cueball.rect.centery
        #self.angle = math.degrees(math.atan2(x, y)) + 90
        #print(self.angle)
        
        #self.image = pygame.transform.rotate(self.orig_image, self.angle)
        #self.set_position(curr_x, curr_y)
        #self.rect = self.image.get_rect()
        #self.rect.x = curr_x
        #self.rect.y = curr_y
