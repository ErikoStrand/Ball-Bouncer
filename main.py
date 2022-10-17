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
SQUARE_AMOUNT = 100
BALL_SPEED = 600
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
        self.trail_len = 15
        self.yellow = Color("yellow")
        self.colors = list(self.yellow.range_to(Color("red"),self.trail_len))   
        
    def update(self, dt):
        if self.y < 0 + self.width/2:
            self.angley -= 180
        if self.y > self.displayh - self.width/2:
            self.angley += 180
        if self.x < 0:
            self.anglex -= 180
        if self.x > self.displayw - self.width:
            self.anglex += 180     
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
                
                pygame.draw.circle(self.display, self.color, (trail.x + self.width / 2, trail.y), self.width / 2)    
        #pygame.draw.rect(self.display, (170, 170, 170), self.rect)
        
while True:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()     
        if event.type == pygame.MOUSEBUTTONDOWN:
            sys.exit()
    if len(SQUARES) <= SQUARE_AMOUNT:
        SQUARES.append(player(random.randint(100, WIDTH - 100),random.randint(100, WIDTH - 100), 50, 50, BALL_SPEED, random.randint(0, 360), DISPLAY, WIDTH, HEIGHT))   
        
    for item in SQUARES:
        item.update(dt)
               
    DISPLAY.fill((134, 123, 42)) 
      
    for item in SQUARES:
        item.draw()
    pygame.display.flip()