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
BALL_COLORS = []
EXPLOSION_COLORS = [] 
BALL_SIZE = 200
BALL_AMOUNT = 2
BALL_SPEED = 300
TRAIL_SIZE = int(BALL_SIZE/2.105263)
FRAGMENT_AMOUNT = 25
FRAGMENT_SIZE = 25
EXPLOSION_SIZE =  1000
EXPLOSION_EXPANSION = 10
EXPLOSION_DECAY = 25
DELETE_BARRIER = 100
EXPLOSIONS_TOGGLE = 1

COLOR_RANGE = (10)
OLD_RANGE = (EXPLOSION_SIZE + 20)  

def get_colours():
    gray = Color("#545c64")
    btg = list(gray.range_to(Color("#000000"), 6))  
    red = Color("#f9e200")
    rty = list(red.range_to(Color("#e40b00"), 7))
    
    yellow = Color("#f9e200")
    colors = list(yellow.range_to(Color("#e40b00"), TRAIL_SIZE))  
    for rty in rty:
        EXPLOSION_COLORS.append(ImageColor.getrgb(str(rty)))
    for btg in btg:
        EXPLOSION_COLORS.append(ImageColor.getrgb(str(btg)))
    for bg in colors:
        BALL_COLORS.append(ImageColor.getrgb(str(bg)))
            
def draw_text(text, font_size, x, y):
    font = pygame.font.Font("AldotheApache.ttf", font_size)
    draw = font.render(str(text), False, (255, 255, 255))
    DISPLAY.blit(draw, (x, y))
            
class explosion:
    def __init__(self, display, x, y, width, fragments, colors):
        self.expansion = EXPLOSION_EXPANSION
        self.fragments_loc = []
        self.fragment_color = []
        self.size = 0
        self.display = display
        self.x = x
        self.y = y
        self.decay = EXPLOSION_DECAY
        self.width = width
        self.fragments = fragments
        self.spawn_fragments = True
        self.colors = colors
                      
    def update(self, dt):
        self.last_size = self.size - 1
        self.size += int(dt * 280 * self.expansion)
            
        if self.spawn_fragments:
            for i in range(FRAGMENT_AMOUNT):
                radius = np.random.randint(self.last_size, self.size + np.random.randint(1, 20))
                angle = np.random.randint(1, 360)
                fx = int(self.x + radius * math.cos(math.radians(angle)))
                fy = int(self.y + radius * math.sin(math.radians(angle)))
                self.fragments_loc.append((fx, fy))
                #color
                
                distp = math.hypot(fx - self.x, fy - self.y)
                dist = (((distp) * COLOR_RANGE) / OLD_RANGE)
                self.color = self.colors[int(dist)]
                self.fragment_color.append(self.color)
                
        if self.size >= EXPLOSION_SIZE:
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
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self, dt):    
        self.x = self.x + dt*self.speed*(math.cos(math.radians(self.anglex)))
        self.y = self.y + dt*self.speed*(math.sin(math.radians(self.angley)))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        if len(self.lastpos) > self.trail_len:
            self.lastpos.pop(0) 
        self.lastpos.append(self.rect.center)
        
        
    def draw(self):
        self.lenght = len(self.lastpos)  
        self.lenght_color = len(self.colors)
        for count, trail in enumerate(self.lastpos):
            if 0 < count < self.lenght - 1:
                pygame.draw.circle(self.display, self.colors[count], trail, (self.width / 2 - self.lenght + count))    
                
get_colours()
FPS_UPDATE = 1
diff = 0               
while 1:
    if FPS_UPDATE:
        start_fps = time.time()
        FPS_UPDATE = 0
        
    start = time.time()
    dt = clock.tick(240) / 250
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            sys.exit()
    if BALL_AMOUNT > len(SQUARES):
        spawnX = np.random.randint(100, WIDTH - 100)
        spawnY = np.random.randint(100, HEIGHT - 100)
        SQUARES.append(player(spawnX , spawnY, BALL_SIZE, BALL_SIZE, BALL_SPEED, np.random.randint(0, 360), DISPLAY, WIDTH, HEIGHT, BALL_COLORS))   
   
    # update  verkar lagga den   
    for item in SQUARES:
        if item.y < 0:
            item.angley -= 180
        elif item.y > item.displayh - item.width:
            item.angley += 180
        elif item.x < 0:
            item.anglex -= 180
        elif item.x > item.displayw - item.width:
            item.anglex += 180 
            
        if item.y < -DELETE_BARRIER:
            SQUARES.remove(item)
        elif item.y > item.displayh - item.width + DELETE_BARRIER:
            SQUARES.remove(item)
        elif item.x < -DELETE_BARRIER:
            SQUARES.remove(item)
        elif item.x > item.displayw - item.width + DELETE_BARRIER:
            SQUARES.remove(item)
            
        #collision
        if EXPLOSIONS_TOGGLE:   
            for test in SQUARES:
                if test != item:
                    if pygame.Rect.colliderect(item.rect, test.rect):
                        EXPLOSIONS.append(explosion(DISPLAY, item.rect.centerx, item.rect.centery, FRAGMENT_SIZE, FRAGMENT_AMOUNT, EXPLOSION_COLORS))
                        SQUARES.remove(test)
                        try:
                            SQUARES.remove(item)
                        except Exception as e: print(e)
           
               
        item.update(dt)
        
    for explode in EXPLOSIONS:
        explode.update(dt)
        if explode.width <= 0:
            EXPLOSIONS.remove(explode)
            
    DISPLAY.fill(BACKGROUND) 
    
        
    for explode in EXPLOSIONS:
        explode.draw()  
    for item in SQUARES:
        item.draw()
    stop = time.time()
    
    if time.time() - start_fps > 0.25:
        diff = stop - start
        FPS_UPDATE = 1
        
    if diff > 0:
        FPS = int(1/diff)
        draw_text(FPS, 40, 0, 0)
    pygame.display.flip()