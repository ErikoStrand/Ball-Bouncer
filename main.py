import pygame
import sys
import math
import random
from colour import Color
from PIL import ImageColor
pygame.init()

clock = pygame.time.Clock()
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
SQUARES = []
EXPLOSIONS = []
BALL_SIZE = 50
TRAIL_SIZE = 20
FRAGMENT_AMOUNT = 100
EXPLOSION_SIZE = int(BALL_SIZE * 2)
SQUARE_AMOUNT = 5
BALL_SPEED = 600
class explosion:
    def __init__(self, display, x, y, width, fragments):
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
        self.gray = Color("gray")
        self.btg = list(self.gray.range_to(Color("black"), 4))  
        self.red = Color("red")
        self.rty = list(self.red.range_to(Color("yellow"), 9))  
        self.colors = []
        for rty in self.rty:
            self.colors.append(rty)
        for btg in self.btg:
            self.colors.append(btg)
            
            
    def update(self, dt):
        self.last_size = self.size
        self.size += int(dt * 280 * self.expansion)
        
        if self.size >  EXPLOSION_SIZE:
            self.size = EXPLOSION_SIZE
            
        if self.spawn_fragments:
            for i in range(4):
                radius = random.randint(self.last_size, self.size)
                angle = random.randint(1, 360)
                fx = int(self.width/2 + radius * math.cos(math.radians(angle)))
                fy = int(self.width/2 + radius * math.sin(math.radians(angle)))
                self.fragments_loc.append((fx + self.x, fy + self.y))
                dist = math.hypot(self.x - fx - self.x , self.y - fy - self.y) / 10
                dist = int(round(dist, 0))
                hex = self.colors[dist]
                self.color = ImageColor.getrgb(str(hex))
                self.fragment_color.append(self.color)
                
        if len(self.fragments_loc) >= FRAGMENT_AMOUNT:
            self.spawn_fragments = False
            
        self.width = self.width - (self.decay * dt)
        
    def draw(self):
        for count, frag in enumerate(self.fragments_loc):
            pygame.draw.circle(self.display, self.fragment_color[count], frag, self.width)
        
class player:
    def __init__(self, x, y, width, height, speed, starting_angle, display, displayw, displayh):
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
        self.yellow = Color("yellow")
        self.colors = list(self.yellow.range_to(Color("red"),self.trail_len))   
        
    def update(self, dt):    
        self.x = self.x + dt*self.speed*(math.cos(math.radians(self.anglex)))
        self.y = self.y + dt*self.speed*(math.sin(math.radians(self.angley)))
        self.rect = pygame.Rect(self.x, self.y - self.width/2, self.width, self.height)
        
        if len(self.lastpos) > self.trail_len:
            self.lastpos.pop(0) 
        self.lastpos.append(pygame.Rect(self.x, self.y, self.width, self.height))
        
    def draw(self):
        for count, trail in enumerate(self.lastpos):
            if 0 < count < len(self.colors) - 1:
                hex = self.colors[count]
                self.color = ImageColor.getrgb(str(hex))
                
                pygame.draw.circle(self.display, self.color, (trail.x + self.width / 2, trail.y), self.width / 2 - len(self.lastpos) + count)    
                
        
while True:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()     
        if event.type == pygame.MOUSEBUTTONDOWN:
            sys.exit()
    if SQUARE_AMOUNT > len(SQUARES):
        SQUARES.append(player(random.randint(100, WIDTH - 100),random.randint(100, WIDTH - 100), BALL_SIZE, BALL_SIZE, BALL_SPEED, random.randint(0, 360), DISPLAY, WIDTH, HEIGHT))   
   
    # update    
    for item in SQUARES:
        if item.y < 0 + item.width/2:
            item.angley -= 180
            EXPLOSIONS.append(explosion(DISPLAY, item.x, item.y, int(BALL_SIZE/2), FRAGMENT_AMOUNT))
        if item.y > item.displayh - item.width/2:
            item.angley += 180
            EXPLOSIONS.append(explosion(DISPLAY, item.x, item.y, int(BALL_SIZE/2), FRAGMENT_AMOUNT))
        if item.x < 0:
            item.anglex -= 180
            EXPLOSIONS.append(explosion(DISPLAY, item.x, item.y, int(BALL_SIZE/2), FRAGMENT_AMOUNT))
        if item.x > item.displayw - item.width:
            item.anglex += 180 
            EXPLOSIONS.append(explosion(DISPLAY, item.x, item.y, int(BALL_SIZE/2), FRAGMENT_AMOUNT))
            
        if item.y < -10 + item.width/2:
            SQUARES.remove(item)
        if item.y > item.displayh - item.width/2 + 10:
            SQUARES.remove(item)
        if item.x < -10:
            SQUARES.remove(item)
        if item.x > item.displayw - item.width + 10:
            SQUARES.remove(item)
            
            
        item.update(dt)
        
    for explode in EXPLOSIONS:
        explode.update(dt)
        if explode.width < 2:
            EXPLOSIONS.remove(explode)
            
    DISPLAY.fill((134, 123, 42)) 
    for explode in EXPLOSIONS:
        explode.draw()  
    for item in SQUARES:
        item.draw()
    pygame.display.flip()