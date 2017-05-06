import pygame
from pygame import *
from pygame.locals import *
from sprites import *
import os

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((TABLE_WIDTH,TABLE_HEIGHT))
    pygame.display.set_caption('Billiards')
    pygame.mouse.set_visible(0)
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))
    
    screen.blit(background,(0,0))
    pygame.display.flip()
    
    clock = pygame.time.Clock()
    table = Table()
    balls = Balls()
    balls.reset()
    
    going = True
    while going:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
        
        screen.blit(background,(0,0))
        table.draw(screen)
        balls.draw(screen)
        pygame.display.flip()
    
    pygame.quit()