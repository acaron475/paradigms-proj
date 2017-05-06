import pygame
from pygame import *
from pygame.locals import *
from sprites import *
import os
from pip.download import _check_download_dir

if __name__ == '__main__':
# Main set up
    pygame.init()
    screen = pygame.display.set_mode((TABLE_WIDTH,TABLE_HEIGHT))
    pygame.display.set_caption('Billiards')
    pygame.mouse.set_visible(0)
    pygame.key.set_repeat(100,10)
    
# Create background    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))
    
    screen.blit(background,(0,0))
    pygame.display.flip()
    clock = pygame.time.Clock()
 
# Create sprite Objects 
    table = Table()
    stick = Stick()
    balls = Balls()
    balls.reset()
    stick.set_position(balls.balls[0].rect.centerx,balls.balls[0].rect.centery)
    
# Start Main Loop
    going = True
    shooting = False
    while going:
        clock.tick(60)
        
        if shooting == False: #If Ball has yet to be shot 
            for event in pygame.event.get():
                if event.type == QUIT:
                    going = False
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    going = False
                elif event.type == KEYDOWN and event.key == K_UP: #Draw back stick
                    stick.pull()
                elif event.type == KEYDOWN and event.key == K_DOWN: #Release stick forward
                    stick.release()
                elif event.type == KEYDOWN and event.key == K_SPACE and stick.power > 0: #Take shot
                    shooting = True
        else: #Ball is being shot
            for event in pygame.event.get():
                if event.type == QUIT:
                    going = False
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    going = False
                elif event.type == MOUSEBUTTONDOWN and event.button == 1: #Temp way to quit shooting loop
                    shooting = False
        
        #Draw Sprites
        screen.blit(background,(0,0))
        table.draw(screen)
        balls.draw(screen)
        
        #Handle drawing of stick sprite --- TODO: Add in balls being effected       
        if(shooting == False):
            stick.draw(screen)
        else: #Stick is shooting
            if stick.old_x == stick.rect.x and stick.old_y == stick.rect.y: #Stick has hit ball
                # set speed and power of cueball
                # with data from the stick
                balls.balls[0].speed = stick.power
                balls.balls[0].angle = stick.angle
                stick.power = 0
                stick.draw(screen)
                shooting = False
            else: #Stick has not yet hit ball
                stick.shoot()
                stick.draw(screen)

        if shooting == False:
            if balls.done() == True:
                #if we made a shot and now the balls are done moving
                #reset the stick and set shooting to false
                stick.set_position(balls.balls[0].rect.centerx, balls.balls[0].rect.centery)
                shooting = False

        pygame.display.flip()
        balls.tick()
        
    pygame.quit()
