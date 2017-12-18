from pygame.locals import *
import pygame
import pygame.time
import random
from PIL import Image
#import time
from enum import Enum


class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


class Head:    
    
    def __init__(self, App_Self, Apple_Self):
        self._App = App_Self
        self._Apple = Apple_Self

        self.x =  ((self._App.windowWidth / self._App.imagesWidth) / 2 )* self._App.imagesWidth 
        self.y =  ((self._App.windowHeight / self._App.imagesHeight) / 2 )* self._App.imagesHeight
        
        self.direction = Direction.RIGHT
        self.axisSize = self._App.windowWidth
        
        self.speed = self._App.imagesWidth

    def posSpeed(self):
        if self.speed < 0 : self.speed = self.speed * (-1)

    def negSpeed(self):
        if self.speed > 0 : self.speed = self.speed * (-1)  

    def move(self):

        if self.direction == Direction.RIGHT or self.direction == Direction.LEFT:
            self.x = (self.x + self.speed) % self.axisSize
        
        if self.direction == Direction.UP or self.direction == Direction.DOWN:
            self.y = (self.y + self.speed) % self.axisSize
    
    def isEating(self):
        return self.x == self._Apple.x and self.y == self._Apple.y 


class Tail:

    def __init__(self, App_Self, Head_Self):
        self._App = App_Self
        self._Head = Head_Self
        
        self.x = self._Head.x
        self.y = self._Head.y


class Apple:

    def __init__(self, App_Self):
        self._App = App_Self

        self.rand_x = random.randrange(self._App.windowWidth) 
        self.rand_y = random.randrange(self._App.windowHeight)

        self.x = self.rand_x - (self.rand_x % 50)
        self.y = self.rand_y - (self.rand_y % 50)

    def new_coordinates(self):
        
        flag = True
        
        while flag:

            self.rand_x = random.randrange(self._App.windowWidth)
            self.rand_y = random.randrange(self._App.windowHeight)

            self.x = self.rand_x - (self.rand_x % 50)
            self.y = self.rand_y - (self.rand_y % 50)

            flag = self._App.is_occupied(self.x, self.y)


class App:    

    def __init__(self):
        self.imagesWidth = Image.open("green_square.png").size[0]
        self.imagesHeight = Image.open("green_square.png").size[1]
        self.windowWidth = (self.imagesWidth * 15)
        self.windowHeight = (self.imagesHeight * 2)
        
        self._running = True
        self._display_surf = None
        self._image_apple = None
        self._image_head = None


        self.frame_rate = 25
        self.apple = Apple(self)        
        self.head = Head(self, self.apple)
        self.tail = []
        for i in range(0, 3):
            self.tail.append(Tail(self, self.head))
        
    def is_occupied(self, x, y):
        for t in self.tail:
            if t.x == x and t.y == y: return True

        if self.head.x == x and self.head.y == y : return True
        
        return False

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
 
        pygame.display.set_caption('Snake')
        self._running = True
        self._image_head = pygame.image.load("green_square.png").convert()
        self._image_tail = pygame.image.load("green_square.png").convert()
        self._image_apple = pygame.image.load("red_circle.png").convert()
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        pass
 
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self._display_surf.blit(self._image_head,(self.head.x,self.head.y))
        for t in self.tail:
            self._display_surf.blit(self._image_tail,(t.x,t.y))
        self._display_surf.blit(self._image_apple,(self.apple.x,self.apple.y))
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        self.on_loop()
        self.on_render()

        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed() 
 
            if (keys[K_RIGHT] and self.head.direction != Direction.LEFT):
                self.head.direction = Direction.RIGHT
                self.head.axisSize = self.windowWidth
                self.head.posSpeed()
            elif (keys[K_LEFT] and self.head.direction != Direction.RIGHT):
                self.head.direction = Direction.LEFT
                self.head.axisSize = self.windowWidth
                self.head.negSpeed()
            elif (keys[K_UP] and self.head.direction != Direction.DOWN):
                self.head.direction = Direction.UP
                self.head.axisSize = self.windowHeight
                self.head.negSpeed()
            elif (keys[K_DOWN] and self.head.direction != Direction.UP):
                self.head.direction = Direction.DOWN
                self.head.axisSize = self.windowHeight
                self.head.posSpeed()
            elif (keys[K_ESCAPE]):
                self._running = False

            #Reverse foreach. Update tail position from the bottom to the top
            for i in (reversed(range(len(self.tail)))):
                if i == 0:
                    self.tail[i].x = self.head.x
                    self.tail[i].y = self.head.y
                else:
                    self.tail[i].x = self.tail[i-1].x
                    self.tail[i].y = self.tail[i-1].y            

            self.head.move()

            for t in self.tail:
                if self.head.x == t.x and self.head.y == t.y:
                    print("You lose...")
                    
                    self._running = False
            
            if self.head.isEating():
                self.apple.new_coordinates()
                self.tail.append(Tail(self, self.head))
                self.tail[len(self.tail) - 1].x = 0
                self.tail[len(self.tail) - 1].y = 0
                #self.frame_rate += 1                                   #Not the best way to speed up

            #pygame.time.wait(250)                                      #Milliseconds
            pygame.time.Clock().tick(self.frame_rate)                   #Frame for second

            if len(self.tail) == ((self.windowHeight / self.imagesHeight * self.windowWidth / self.imagesWidth) - 1):
                print("Size snake = "),
                print len(self.tail) + 1
                print("You WIN!!!")

                self._running = False


            self.on_loop()
            self.on_render()

        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()