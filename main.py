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
pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN])
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
#BACKGROUND = (112, 123, 138)
BACKGROUND = (0, 0, 0)
SQUARES = []
EXPLOSIONS = []
BALL_SIZE = 50
TRAIL_SIZE = 20
FRAGMENT_AMOUNT = 100
EXPLOSION_SIZE = 100
SQUARE_AMOUNT = 100
BALL_SPEED = 500
BALL_COLORS = []
EXPLOSION_COLORS = []

def get_colours():
    gray = Color("#545c64")
    btg = list(gray.range_to(Color("#000000"), 6))  
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
    def __init__(self, display, x, y, width, fragments, colors):
        self.expansion = 1
        self.fragments_loc = []
        self.fragment_color = []
        self.size = 0
        self.display = display
        self.x = x
        self.y = y
        self.decay = 25
        self.width = width
        self.fragments = fragments
        self.spawn_fragments = True
        self.colors = colors
                      
    def update(self, dt):
        self.last_size = self.size - 1
        self.size += int(dt * 280 * self.expansion)
        
        # sets max size of explosion
        if self.size >  EXPLOSION_SIZE:
            self.size = EXPLOSION_SIZE
            
        # might cause lag try fix
        if self.spawn_fragments:
            for i in range(4):
                radius = np.random.randint(self.last_size, self.size + np.random.randint(1, 20))
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
                
get_colours()                
while 1:
    start = time.time()
    dt = clock.tick(120) / 500
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            sys.exit()
    if SQUARE_AMOUNT > len(SQUARES):
        spawnX = np.random.randint(100, WIDTH - 100)
        spawnY = np.random.randint(100, HEIGHT - 100)
        SQUARES.append(player(spawnX , spawnY, BALL_SIZE, BALL_SIZE, BALL_SPEED, np.random.randint(0, 360), DISPLAY, WIDTH, HEIGHT, BALL_COLORS))   
   
    # update    
    for item in SQUARES:
        if item.y < 0 + item.width/2:
            item.angley -= 180
            EXPLOSIONS.append(explosion(DISPLAY, item.x, item.y, int(BALL_SIZE/2), FRAGMENT_AMOUNT, EXPLOSION_COLORS))
        elif item.y > item.displayh - item.width/2:
            item.angley += 180
            EXPLOSIONS.append(explosion(DISPLAY, item.x, item.y, int(BALL_SIZE/2), FRAGMENT_AMOUNT, EXPLOSION_COLORS))
        elif item.x < 0:
            item.anglex -= 180
            EXPLOSIONS.append(explosion(DISPLAY, item.x, item.y, int(BALL_SIZE/2), FRAGMENT_AMOUNT, EXPLOSION_COLORS))
        elif item.x > item.displayw - item.width:
            item.anglex += 180 
            EXPLOSIONS.append(explosion(DISPLAY, item.x, item.y, int(BALL_SIZE/2), FRAGMENT_AMOUNT, EXPLOSION_COLORS))
            
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
            if test != item:
                if pygame.Rect.colliderect(item.rect, test.rect):
                    EXPLOSIONS.append(explosion(DISPLAY, item.x, item.y, int(BALL_SIZE/2), FRAGMENT_AMOUNT, EXPLOSION_COLORS))
                    SQUARES.remove(test)
                    try:
                        SQUARES.remove(item)
                    except Exception as e: print(e)
           
               
        item.update(dt)
        
    for explode in EXPLOSIONS:
        explode.update(dt)
        if explode.width < 2:
            EXPLOSIONS.remove(explode)
            
    DISPLAY.fill(BACKGROUND) 
    
    for explode in EXPLOSIONS:
        explode.draw()  
    for item in SQUARES:
        item.draw()
        
    pygame.display.flip()
    stop = time.time()
    print(str(round(stop - start, 5)) + "s")