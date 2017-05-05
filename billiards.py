import pygame
from pygame import *
from pygame.locals import *
from sprites import *
import os


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
    table = Table('table.png')
    cueball = Ball('ball_16.png')
    ball = Ball('ball_1.png')
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