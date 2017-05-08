import pygame
from pygame import *
from pygame.locals import *
from classes import *
import os
import sys

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
    data = {}
    data['background'] = background
    data['screen'] = screen
    data['table'] = Table()
    #walls = Walls()
    stick = Stick()
    data['stick'] = stick
    balls = Balls()
    data['balls'] = balls
    data['balls'].reset()
    stick.set_position(balls.balls[0].rect.centerx,balls.balls[0].rect.centery)
    player = Player(int(sys.argv[2]),str(sys.argv[1]),balls)
    data['player'] = player
    data['shooting'] = False
    player.startConnection(data)
    
# Start Main Loop
def game_loop(dict):
    player = dict['player']
    balls = dict['balls']
    stick = dict['stick']
    table = dict['table']
    background = dict['background']
    screen = dict['screen']
    shooting = dict['shooting']
#    clock = dict['clock']
    
    if player.turn == True and player.connected == True:
#        for i,ball in player.balls.balls:
#            balls.balls[i].rect.x = ball.rect.x
#            balls.balls[i].rect.y = ball.rect.y
        balls = player.balls
            
        for event in pygame.event.get():
            if event.type == QUIT:
                stop()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                stop()
            elif event.type == KEYDOWN and event.key == K_w: #Draw back stick
                stick.pull()
            elif event.type == KEYDOWN and event.key == K_s: #Release stick forward
                stick.release()
            elif event.type == KEYDOWN and event.key == K_a:
                stick.angle += math.radians(5)
            elif event.type == KEYDOWN and event.key == K_d:
                stick.angle -= math.radians(5)
            elif event.type == KEYDOWN and event.key == K_SPACE and stick.power > 0: #Take shot
                # set speed and power of cueball
                # with data from the stick
                stick.shoot()
                balls.balls[0].speed = stick.power/5
                balls.balls[0].angle = stick.angle #(radians)
                stick.power = 0
                shooting = True
                dict['shooting'] = True

        #Draw Sprites
        screen.blit(background,(0,0))
        table.draw(screen)
        balls.draw(screen)
        stick.draw(screen,balls.balls[0],player.turn)

        if stick.power == 0 and shooting == True:
            if balls.done() == True:
                #if we made a shot and now the balls are done moving
                #reset the stick and set shooting to false
                player.sendMove()
                stick.image = stick.orig_image
                shooting = False
                dict['shooting'] = shooting
        
        if shooting or player.turn == False:
            stick.image = stick.hidden_image
        else:
            stick.image = stick.orig_image
            if stick.power == 0:
                stick.set_position(balls.balls[0].rect.centerx, balls.balls[0].rect.centery)            

        pygame.display.flip()
        balls.tick()
        stick.tick(balls.balls[0])
        balls.collisions()
    else:
        for event in pygame.event.get():
            if event.type == QUIT:
                stop()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                stop()
        
        if player.connected == False:
            myfont = pygame.font.SysFont("monospace",15)
            label = myfont.render("WAITING FOR CONNECTION",1,(0,0,0))
            screen.blit(label,(1138/2-11,643))
            
    stick.draw(screen,balls.balls[0],player.turn)            

    dict['player'] = player
    dict['balls'] = balls
    dict['stick'] = stick
    dict['table'] = table
    dict['background'] = background
    dict['screen'] = screen
    dict['shooting'] = shooting

def quit():    
    player.closeConnection()                        
    pygame.quit()
