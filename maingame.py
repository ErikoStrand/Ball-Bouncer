from logging import WARNING
import pygame
import sys
import math
import numpy as np
import time
from colour import Color
from PIL import ImageColor

pygame.init()

clock = pygame.time.Clock()
infoObject = pygame.display.Info()
pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN,pygame.KEYDOWN,pygame.KEYUP])
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = (0, 0, 0)
SQUARES = []
EXPLOSIONS = []
BALL_SIZE = 50
TRAIL_SIZE = 20
FRAGMENT_AMOUNT = 100
EXPLOSION_SIZE = 100
SQUARE_AMOUNT = 10
BALL_SPEED = 500
BALL_COLORS = []
EXPLOSION_COLORS = []
WARNING = []
CharacterX = 50
CharacterY = 50

CharSpeed = 4

CharUp,CharLeft,CharDown,CharRight = False,False,False,False

def draw_text(text, font_size, x, y):
    font = pygame.font.Font("AldotheApache.ttf", font_size)
    a, b = pygame.font.Font.size(font, str(text))
    draw = font.render(str(text), False, (255, 255, 255))
    DISPLAY.blit(draw, (x - a/2, y))


def get_colours():
    gray = Color("#545c64")
    btg = list(gray.range_to(Color("#000000"), 4))  
    red = Color("#f9e200")
    rty = list(red.range_to(Color("#e40b00"), 9))
    
    yellow = Color("#f9e200")
    colors = list(yellow.range_to(Color("#e40b00"), TRAIL_SIZE))  
    for rty in rty:
        EXPLOSION_COLORS.append(ImageColor.getrgb(str(rty)))
    for btg in btg:
        EXPLOSION_COLORS.append(ImageColor.getrgb(str(btg)))
    for bg in colors:
        BALL_COLORS.append(ImageColor.getrgb(str(bg)))
            
class explosion:
    def __init__(self, display, x, y, width, fragments, colors, size):
        self.expansion = 1
        self.fragments_loc = []
        self.fragment_color = []
        self.size = 0
        self.display = display
        self.x = x
        self.y = y
        self.explosion = size
        self.decay = 25
        self.width = width
        self.fragments = fragments
        self.spawn_fragments = True
        self.colors = colors
                      
    def update(self, dt):
        self.last_size = self.size - 1
        self.size += int(dt * 280 * self.expansion)
        
        # sets max size of explosion
        if self.size >  self.explosion:
            self.size = self.explosion
            
        # might cause lag try fix
        if self.spawn_fragments:
            for i in range(4):
                radius = np.random.randint(self.last_size, self.size)
                angle = np.random.randint(1, 360)
                fx = int(self.width/2 + radius * math.cos(math.radians(angle)))
                fy = int(self.width/2 + radius * math.sin(math.radians(angle)))
                self.fragments_loc.append((fx + self.x, fy + self.y))
                dist = math.hypot(self.x - fx - self.x , self.y - fy - self.y) / 10
                dist = int(round(dist, 0))
                self.color = self.colors[dist]
                self.fragment_color.append(self.color)
                
        if len(self.fragments_loc) >= FRAGMENT_AMOUNT:
            self.spawn_fragments = False
            
        self.width = self.width - (self.decay * dt)
    
    def draw(self):
        for count, frag in enumerate(self.fragments_loc):
            pygame.draw.circle(self.display, self.fragment_color[count], frag, self.width)
        
class player:
    def __init__(self, x, y, width, height, speed, starting_angle, display, displayw, displayh, colors):
        self.lastpos = []
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.anglex = starting_angle
        self.angley = starting_angle
        self.displayw = displayw
        self.displayh = displayh
        self.display = display
        self.trail_len = TRAIL_SIZE
        self.colors = colors   
        self.rect = pygame.Rect(self.x, self.y - self.width/2, self.width, self.height)
    
    def update(self, dt):    
        self.x = self.x + dt*self.speed*(math.cos(math.radians(self.anglex)))
        self.y = self.y + dt*self.speed*(math.sin(math.radians(self.angley)))
        self.rect = pygame.Rect(self.x, self.y - self.width/2, self.width, self.height)
        
        if len(self.lastpos) > self.trail_len:
            self.lastpos.pop(0) 
        self.lastpos.append(pygame.Rect(self.x, self.y, self.width, self.height))
        
        
    def draw(self):
        self.lenght = len(self.lastpos)  
        self.lenght_color = len(self.colors)
        for count, trail in enumerate(self.lastpos):
            if 0 < count < self.lenght - 1:
                pygame.draw.circle(self.display, self.colors[count], (trail.x + self.width / 2, trail.y), self.width / 2 - self.lenght + count)    
class warning:
    def __init__(self, x, y, time, timetime, angle):
        self.x = x
        self.y = y
        self.time = time 
        self.timetime = timetime
        self.angle = angle
        self.fx = int(self.x + 100 * math.cos(math.radians(self.angle)))
        self.fy = int(self.y + 100 * math.sin(math.radians(self.angle))) 
    def update(self, timetime):  
        if timetime - self.timetime > self.time:
            SQUARES.append(player(self.x , self.y, BALL_SIZE, BALL_SIZE, BALL_SPEED, self.angle, DISPLAY, WIDTH, HEIGHT, BALL_COLORS))
            return True
    def draw(self):  
        pygame.draw.line(DISPLAY, (255, 0, 0), (self.x, self.y), (self.fx, self.fy), 5)
        pygame.draw.circle(DISPLAY, (255, 0, 0), (self.x, self.y), 25)                         
get_colours()
start = time.time()               
while 1:
    objectPlayer = pygame.Rect(CharacterX,CharacterY, 25,25)
    dt = clock.tick(120) / 500
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                CharUp = True
            if event.key == pygame.K_a:
                CharLeft = True
            if event.key == pygame.K_s:
                CharDown = True
            if event.key == pygame.K_d:
                CharRight = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                CharUp = False
            if event.key == pygame.K_a:
                CharLeft = False
            if event.key == pygame.K_s:
                CharDown = False
            if event.key == pygame.K_d:
                CharRight = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            sys.exit()
    if SQUARE_AMOUNT > len(SQUARES):
        spawnX = np.random.randint(100, WIDTH - 100)
        spawnY = np.random.randint(100, HEIGHT - 100)
        if SQUARE_AMOUNT > len(WARNING):
            if  not objectPlayer.collidepoint((spawnX, spawnY)):
                WARNING.append(warning(spawnX, spawnY, 1, time.time(), np.random.randint(0, 360)))
                #SQUARES.append(player(spawnX , spawnY, BALL_SIZE, BALL_SIZE, BALL_SPEED, np.random.randint(0, 360), DISPLAY, WIDTH, HEIGHT, BALL_COLORS))   
   
    # update    
    for item in SQUARES:
        if item.y < 0 + item.width/2:
            item.angley -= 180
        elif item.y > item.displayh - item.width/2:
            item.angley += 180
        elif item.x < 0:
            item.anglex -= 180
        elif item.x > item.displayw - item.width:
            item.anglex += 180 
            
        if item.y < -10 + item.width/2:
            SQUARES.remove(item)
        elif item.y > item.displayh - item.width/2 + 10:
            SQUARES.remove(item)
        elif item.x < -10:
            SQUARES.remove(item)
        elif item.x > item.displayw - item.width + 10:
            SQUARES.remove(item)
            
        #collision   
        for test in SQUARES:
            if pygame.Rect.colliderect(test.rect,objectPlayer):
                start = time.time()
                EXPLOSIONS.append(explosion(DISPLAY, objectPlayer.x, objectPlayer.y, int(BALL_SIZE/2), FRAGMENT_AMOUNT, EXPLOSION_COLORS, EXPLOSION_SIZE))
                SQUARES.remove(test)
            if test != item:
                if pygame.Rect.colliderect(item.rect, test.rect):
                    EXPLOSIONS.append(explosion(DISPLAY, item.x, item.y, int(BALL_SIZE/2), FRAGMENT_AMOUNT, EXPLOSION_COLORS, EXPLOSION_SIZE))
                    SQUARES.remove(test)
                    try:
                        SQUARES.remove(item)
                    except Exception as e: print(e)
           
               
        item.update(dt)
    for warnings in WARNING:
        if warnings.update(time.time()):
            WARNING.remove(warnings)
            
    for explode in EXPLOSIONS:
        explode.update(dt)
        if explode.width < 2:
            EXPLOSIONS.remove(explode)
            
    DISPLAY.fill(BACKGROUND)
    draw_text(int(round(time.time() - start, 0)), 300, WIDTH/2, HEIGHT/3 + 100) 
    pygame.draw.rect(DISPLAY, (255,255,255), objectPlayer)
    for explode in EXPLOSIONS:
        explode.draw()  
    for item in SQUARES:
        item.draw()
    for warnings in WARNING:
        warnings.draw()
    pygame.display.flip()
    
    
    if CharUp:
        CharacterY -=50*dt*CharSpeed
    if CharLeft:
        CharacterX -=50*dt*CharSpeed
    if CharDown:
        CharacterY +=50*dt*CharSpeed
    if CharRight:
        CharacterX +=50*dt*CharSpeed
    