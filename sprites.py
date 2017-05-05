import pygame
from pygame import *
from pygame.locals import *
import math
import os

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

class Ball(sprite.Sprite):
    def __init__(self,image):
        sprite.Sprite.__init__(self)
        self.image,self.rect = load_image(image,-1)
        self.speed = 0
        self.angle = 0
        
    def set_position(self,x,y):
        self.rect.x = x
        self.rect.y = y
        
    def draw(self,surface):
        surface.blit(self.image,self.rect)
        
class Table(sprite.Sprite):
    def __init__(self,image):
        sprite.Sprite.__init__(self)
        self.image,self.rect = load_image(image)

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