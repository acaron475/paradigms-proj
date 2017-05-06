import pygame
from pygame import *
from pygame.locals import *
import math
import os

TABLE_HEIGHT = 643
TABLE_WIDTH = 1138
BALL_RADIUS = 35

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

class Balls():
    def __init__(self):
        self.balls = [Ball('ball_16.png',0)]
        for i in range(1,16):
            ball = Ball('ball_' + str(i) + '.png',i)
            self.balls.append(ball)
    
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
        
class Table(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image,self.rect = load_image('table.png')

    def draw(self,surface):
        surface.blit(self.image,self.rect)

class Stick(sprite.Sprite):
    def __init__(self,image):
        sprite.Sprite.__init__(self)
        self.image,self.rect = load_image(image)
        self.power = 0
        self.angle = 0
        
    def draw(self,surface):
        surface.blit(self.image,self.rect)