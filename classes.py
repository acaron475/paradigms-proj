import pygame
from pygame import *
from pygame.locals import *
import math
import os
from math import atan2
import client
import json
from client import *

#Constants
TABLE_HEIGHT = 643
TABLE_WIDTH = 1138
BALL_RADIUS = 35/2
FRICTION = 0.98
ELASTICITY = 0.75
PLAYER1_PORT = 40129
PLAYER2_PORT = 41129

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

#Class to hold player's info
class Player():
    def __init__(self,port,addr,balls):
        if port == PLAYER1_PORT:
            self.turn = True
            self.num = 1
        else:
            self.turn = False
            self.num = 2
        self.port = port
        self.addr = addr
        self.connected = False
        self.balls = balls
        self.team = ""
        self.justScored = False
        self.scoreTotal = 0
        self.gameover = False
        self.you_lose_image,temp = load_image("you_lost.png",(255,255,0))
        self.you_win_image,temp = load_image("you_won.png",(255,255,0))
        self.other_lose_image,temp = load_image("other_lost.png",(255,255,0))
        self.other_win_image,temp = load_image("other_won.png",(255,255,0))
        self.stripes_image,temp = load_image("stripes.png",-1)
        self.solids_image,temp = load_image("solids.png",-1)
        self.hidden_team_image,temp = load_image("hidden_team.png",-1)
        self.endImage = self.you_win_image
        self.teamImage = self.hidden_team_image
    
    def startConnection(self,data):
        self.client = Client(self,data)
        self.client.startConnection()
        
    def closeConnection(self):
        self.connection.transport.loseConnection()
    
    def sendMove(self,gameover=None):
        data = [self.justScored,[],self.team]
        for ball in self.balls.balls:
            data[1].append([ball.rect.x,ball.rect.y,ball.scored])        
        if gameover is not None:
            data.append(gameover)
            

        data = json.dumps(data)
        self.connection.transport.write(data.encode('utf-8'))
        if self.justScored == False:
            self.turn = False
        else:
            self.justScored = False
    
    def moveReceived(self,data):
        data = json.loads(data)
        playerScored = data[0]
        for i,arr in enumerate(data[1]):
            x = arr[0]
            y = arr[1]
            scored = arr[2]
            self.balls.balls[i].rect.x = x
            self.balls.balls[i].rect.y = y
            self.balls.balls[i].scored = scored
            if scored:
                self.balls.balls[i].image = self.balls.balls[i].hidden_image
        if self.team == "":
            if data[2] == "stripe":
                self.team = "solid"
                self.teamImage = self.solids_image
            elif data[2] == "solid":
                self.team == "stripe"
                self.teamImage = self.stripes_image
        if playerScored == False:
            self.turn = True
        if len(data) == 4:
            self.gameover(data[3])
    
    def handleScores(self,arr):
        for i,scored in enumerate(arr):
            if scored == 1:
                if i == 8:
                    self.gameover(1)
                elif i == 0:
                    print("scratched")
                    self.cueScratch()
                elif self.team == "":
                    self.justScored = True
                    self.scoreTotal += 1
                    if i < 8:
                        self.team = "solid"
                        self.teamImage = self.solids_image
                    else:
                        self.team = "stripe"
                        self.teamImage = self.stripes_image
                elif self.team == "solid" and i < 8:
                    self.justScored = True
                    self.scoreTotal += 1
                elif self.team == "stripe" and i > 8:
                    self.justScored = True
                    self.scoreTotal += 1

    def cueScratch(self):
        print("resetting from scratch")
        self.balls.balls[0].set_position(3*TABLE_WIDTH/4-27, TABLE_HEIGHT/2)
                    
    def gameover(self,status):
        self.gameover = True
        if status == 1 and self.scoreTotal == 7:
            self.win(status)
        elif status == 0:
            self.win(status)
        else:
            self.lose(status)
                            
    def win(self,status):
        if status == 1:
            self.endImage = self.you_won_image
            self.turn = False
            self.sendMove(-1)
        else:
            self.endImage = self.other_lose_image
            self.turn = False
    
    def lose(self,status):
        if status == 1:
            self.endImage = self.you_lose_image
            self.turn = False
            self.sendMove(0)
        else:
            self.endImage = self.other_won_image
            self.turn = False
            
    def drawGameOver(self,surface):
        self.rect = self.endImage.get_rect()
        self.rect.centerx = TABLE_WIDTH/2
        self.rect.centery = TABLE_HEIGHT/2
        surface.blit(self.endImage,self.rect)
        
    def draw(self,surface):
        self.rect = self.teamImage.get_rect()
        surface.blit(self.teamImage,(100,0))  
        

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
        #return
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
        
        for ball in self.balls:
            ball.speed = 0
            ball.angle = 0
            ball.image = ball.orig_image
            ball.scored = False
          
    def draw(self,surface):
        for ball in self.balls:
            ball.draw(surface)

    # moved all collision detection down to Ball class
    def collisions(self):
        scoreArray = []
        for i,ball in enumerate(self.balls):
            if ball.scored == False:
                scoreTest = ball.pocketCollision()
                ball.wallCollision()
                for ball2 in self.balls[i+1:]:
                    if ball2.scored != True:
                        ball.ballCollision(ball2)
                #scoreTest = ball.pocketCollision()
                if scoreTest == True:
                    scoreArray.append(1)
                else:
                    scoreArray.append(0)
            else:
                scoreArray.append(-1)
        return scoreArray
                    
    # tick in order to have balls move
    def tick(self):
        for ball in self.balls:
            ball.tick()

    def done(self):
        # check if all balls are done moving
        for ball in self.balls:
            if ball.scored == False:    
                if ball.speed != 0:
                    return False
        return True
            
#Class for each game ball
class Ball(sprite.Sprite):
    def __init__(self,image,num):
        sprite.Sprite.__init__(self)
        self.orig_image,temp = load_image(image,-1)
        self.hidden_image,temp = load_image('ball_hidden.png',-1)
        self.image = self.image = self.orig_image
        self.rect = self.image.get_rect()
        self.num = num
        self.speed = 0
        self.angle = 0
        self.scored = False
        
    def set_position(self,x,y):
        self.rect.x = x
        self.rect.y = y
        
    def draw(self,surface):
        surface.blit(self.image,self.rect)
        
    # check and handle collision with walls
    def wallCollision(self):
        x, y = self.rect.centerx, self.rect.centery
        if x+BALL_RADIUS >= 1065 and y+BALL_RADIUS < 530 and y-BALL_RADIUS > 75:
            self.rect.centerx = 1064 - BALL_RADIUS
            self.angle = math.pi-self.angle
        if x-BALL_RADIUS <= 75 and y+BALL_RADIUS < 530 and y-BALL_RADIUS > 75:
            self.rect.centerx = 76 + BALL_RADIUS
            self.angle = math.pi-self.angle
        if y+BALL_RADIUS >=570 and ((x+BALL_RADIUS < 1065 and x-BALL_RADIUS > 600) or (x+BALL_RADIUS <= 525 and x-BALL_RADIUS > 75)):
            self.rect.centery = 569 - BALL_RADIUS
            self.angle = -self.angle
        if y-BALL_RADIUS <= 75 and ((x+BALL_RADIUS < 1065 and x-BALL_RADIUS > 600) or (x+BALL_RADIUS <= 525 and x-BALL_RADIUS > 75)):
            self.rect.centery = 76 + BALL_RADIUS
            self.angle = -self.angle
    
    # check and handle collision with another ball
    def ballCollision(self, other):
        dx = self.rect.centerx - other.rect.centerx
        dy = self.rect.centery - other.rect.centery
        distance = math.hypot(dx, dy) #distance between ball centers
        if distance <= BALL_RADIUS*2: #collision!
            #print("collision ", str(self.num), " ",  str(other.num))
            #print("dx is ", str(dx), " dy is ", str(dy))
            #print("self.speed = ", str(self.speed), "angle = ", str(self.angle))
            #print("other.speed = ", str(other.speed), "angle = ", str(other.angle))
            #calculate angle between balls
            tangent = math.atan2(dy,dx)     
            #tangent = -1*(tangent-math.pi) #convert to our reference
            #print("tangent is ", str(tangent))
            
            #Set new x/y distances ---- Huzzah for wikipedia: https://en.wikipedia.org/wiki/Elastic_collision#Two-dimensional_collision_with_two_moving_objects

            temp = self.speed
            self.speed = other.speed
            other.speed = temp

            angle = 0.5 * math.pi + tangent
            self.rect.centerx += math.sin(angle)
            self.rect.centery -= math.cos(angle)
            other.rect.centerx -= math.sin(angle)
            other.rect.centery += math.cos(angle)
            
            '''new_x1 = other.speed*math.cos(other.angle-tangent)*math.cos(tangent)+self.speed*math.sin(self.angle-tangent)*math.cos(tangent+math.pi/2)
            new_y1 = other.speed*math.cos(other.angle-tangent)*math.sin(tangent)+self.speed*math.sin(self.angle-tangent)*math.sin(tangent+math.pi/2)
            new_x2 = self.speed*math.cos(self.angle-tangent)*math.cos(tangent)+other.speed*math.sin(other.angle-tangent)*math.cos(tangent+math.pi/2)
            new_y2 = self.speed*math.cos(self.angle-tangent)*math.sin(tangent)+other.speed*math.sin(other.angle-tangent)*math.sin(tangent+math.pi/2)
'''
            '''#Turn x/y distances into angle and magnitude
            self.angle = math.atan2(new_y1, new_x1)
            self.speed = math.hypot(new_x1, new_y1)
            other.angle = math.atan2(new_y2, new_x2)
            other.speed = math.hypot(new_x2, new_y2)
'''
''' #print("new self.speed = ", str(self.speed), "angle = ", str(self.angle))
            #print("new other.speed = ", str(other.speed), "angle = ", str(other.angle))
            
        #Try to unstick balls from each other -- TODO: This part is still iffy                             -1\
            #self.rect.centerx += dx
            #while distance < BALL_RADIUS * 2:
'''
'''         dx = (BALL_RADIUS - dx)# / 2
            dy = (BALL_RADIUS - dy)# / 2
            self.rect.centerx += -dx*math.cos(self.angle)#tangent+math.pi/2)
            self.rect.centery += -dy*math.sin(self.angle)#tangent+math.pi/2)
            #other.rect.centerx -= -dx*math.cos(other.angle)#tangent+math.pi/2)
            #other.rect.centery -= -dy*math.sin(other.angle)#tangent+math.pi/2)
     #      dx = self.rect.centerx - other.rect.centerx
     #      dy = self.rect.centery - other.rect.centery
     #      distance = math.hypot(dx, dy)
'''
    def pocketCollision(self):
        corner_pockets = [(53,60),(53,584),(1077,60),(1077,584)]
        side_pockets = [(563,47),(563,594)]
        for coord in corner_pockets:
            dx = self.rect.centerx - coord[0]
            dy = self.rect.centery - coord[1]
            distance = math.hypot(dx, dy)
            if distance < 35:
                self.score()
                print("ball pocketed")
                return True
        for coord in side_pockets:
            dx = self.rect.centerx - coord[0]
            dy = self.rect.centery - coord[1]
            distance = math.hypot(dx, dy)
            if distance < 30:
                self.score()
                print("ball pocketed")
                return True
        return False
                
    def score(self):
        if self.num == 0: #handle cue ball differently -- we still draw it
            self.speed = 0
            self.angle = 0
            return
        self.image = self.hidden_image
        self.scored = True
        self.speed = 0
        self.angle = 0
        self.rect.x = 0
        self.rect.y = 0

    def tick(self):
        #print("speed is ", str(self.speed))
        # cos and sin take the angle in radians -- be careful
        self.rect.x += -1 * self.speed * math.cos(self.angle)
        self.rect.y += -1 * self.speed * math.sin(self.angle)
        # use -1 since top left is origin
        # added "friction" constant to slow ball then hard stop once reaches slow enough
        if self.speed != 0:
            self.speed *= FRICTION
            if self.speed < 1.75:
                 self.speed = 0
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
        self.image,self.rect = load_image('cue_short.png',-1)
        self.hidden_image,temp = load_image('cue_hidden.png',-1)
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
        if self.power < 150:    
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
        self.rect.y = self.old_y
    
    #Function for setting stick in relation to cue ball
    def set_position(self,x,y):
        self.rect.x = x+BALL_RADIUS
        self.rect.y = y - self.rect.height/2
        
    def draw(self,surface,cueball,show):
        cx = cueball.rect.centerx       
        cy = cueball.rect.centery
        x = cx+BALL_RADIUS*2*math.cos(self.angle-math.pi)
        y = cy+BALL_RADIUS*2*math.sin(self.angle-math.pi)
        if not show:
            y = 0
            x = 0
            cx = 0
            cy = 0
            surface.blit(self.hidden_image,self.rect)
        else:
            surface.blit(self.orig_image,self.rect)
        self.line = pygame.draw.line(surface,(0,0,0),(cx,cy),(x,y))

    # Function to update angle of stick -- follows mouse
    def tick(self, cueball):
        pass
#        cx, cy = cueball.rect.centerx, cueball.rect.centery
#        mx, my = pygame.mouse.get_pos()
#
#        self.angle = -1*(math.atan2(my-cy,mx-cx)-math.pi)
#        print(self.angle)
#        self.image = rot_center(self.orig_image, math.degrees(self.angle))        
#        
#        ratio = (int(math.degrees(self.angle)) / 180) % (180)
#        print(ratio)
#        
#        x = cx# + (self.rect.width/2+BALL_RADIUS)*math.cos(self.angle)
#        y = cy# + (self.rect.width/2+BALL_RADIUS)*math.sin(self.angle)
#        self.rect.midleft = (x,y)
#        self.rect.centery = y
#        x -= cueball.rect.centerx
#        y -= cueball.rect.centery
#        self.angle = math.degrees(math.atan2(x, y)) + 90
#        print(self.angle)
#        
#        self.image = pygame.transform.rotate(self.orig_image, self.angle)
#        self.set_position(curr_x, curr_y)
#        self.rect = self.image.get_rect()
#        self.rect.x = curr_x
#        self.rect.y = curr_y

class Message(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.connection_image,temp = load_image('waiting_for_connection.png',-1)
        self.your_turn_image,temp = load_image('your_turn.png',-1)
        self.other_turn_image,temp = load_image("other_players_turn.png",-1)
        self.image = self.connection_image
        self.rect = self.image.get_rect()
        self.rect.x = 680
        self.rect.y = 10
            
    def draw(self,surface):
        surface.blit(self.image,self.rect)
        
    
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    return rot_image
