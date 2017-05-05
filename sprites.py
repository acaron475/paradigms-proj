import pygame
from pygame import *
from pygame.locals import *
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


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1138,643))
    pygame.display.set_caption('Billiards')
    pygame.mouse.set_visible(0)
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))
    
    screen.blit(background,(0,0))
    pygame.display.flip()
    
    clock = pygame.time.Clock()
    table = Table('table_resize.png')
    cueball = Ball('ball_16_resize.png')
    ball = Ball('ball_1_resize.png')
    cueball.set_position(3*table.rect.width/4-27, table.rect.height/2)
    ball.set_position(table.rect.width/4, table.rect.height/2)
    
    going = True
    while going:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
        
        screen.blit(background,(0,0))
        table.draw(screen)
        cueball.draw(screen)
        ball.draw(screen)
        pygame.display.flip()
    
    pygame.quit()