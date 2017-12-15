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


class Player:    
    
    def __init__(self, App_Self, Apple_Self):
        self._App = App_Self
        self._Apple = Apple_Self
        self.x =  ((self._App.windowWidth / self._App.snake.size[0]) / 2 )* self._App.snake.size[0] 
        self.y =  ((self._App.windowHeight / self._App.snake.size[1]) / 2 )* self._App.snake.size[1]
        self.direction = Direction.RIGHT
        self.axisSize = self._App.windowWidth
        self.speed = self._App.snake.size[0]

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

    def __init__(self, App_Self, Player_Self):
        self._App = App_Self
        self._Player = Player_Self
        
        self.x = self._Player.x
        self.y = self._Player.y


class Apple:

    def __init__(self, App_Self):
        self._App = App_Self
        self.rand_x = random.randrange(self._App.windowWidth)
        self.x = self.rand_x - (self.rand_x % 50) #same rand
        self.rand_y = random.randrange(self._App.windowHeight)
        self.y = self.rand_y - (self.rand_y % 50)



class App:    

    def __init__(self):
        self.snake = Image.open("green_square.png")
        self.windowWidth = (self.snake.size[0]*15)
        self.windowHeight = (self.snake.size[1]*11)
        self._running = True
        self.frame_rate = 5
        self._display_surf = None
        self._image_apple = None
        self._image_snake = None
        self.apple = Apple(self)        
        self.player = Player(self, self.apple)
        self.tail = [Tail(self, self.player)] * 3
        
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
 
        pygame.display.set_caption('Snake')
        self._running = True
        self._image_snake = pygame.image.load("green_square.png").convert()
        self._image_tail = pygame.image.load("green_square.png").convert()
        self._image_apple = pygame.image.load("red_circle.png").convert()
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        pass
 
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self._display_surf.blit(self._image_snake,(self.player.x,self.player.y))
        #TODO: Fix. It'seeing only one pieces
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
 
            if (keys[K_RIGHT] and self.player.direction != Direction.LEFT):
                self.player.direction = Direction.RIGHT
                self.player.axisSize = self.windowWidth
                self.player.posSpeed()

            if (keys[K_LEFT] and self.player.direction != Direction.RIGHT):
                self.player.direction = Direction.LEFT
                self.player.axisSize = self.windowWidth
                self.player.negSpeed()

            if (keys[K_UP] and self.player.direction != Direction.DOWN):
                self.player.direction = Direction.UP
                self.player.axisSize = self.windowHeight
                self.player.negSpeed()
 
            if (keys[K_DOWN] and self.player.direction != Direction.UP):
                self.player.direction = Direction.DOWN
                self.player.axisSize = self.windowHeight
                self.player.posSpeed()
 
            if (keys[K_ESCAPE]):
                self._running = False

            #TODO: reverse foreach

            self.tail[1].x = self.tail[2].x
            self.tail[1].y = self.tail[2].y            

            self.tail[0].x = self.tail[1].x
            self.tail[0].y = self.tail[1].y

            self.tail[1].x = self.player.x
            self.tail[1].y = self.player.y

            self.player.move()

            if self.player.isEating():
                self.frame_rate += 1
                



            #pygame.time.wait(250)                                      #Milliseconds
            pygame.time.Clock().tick(self.frame_rate)                   #Frame for second

            self.on_loop()
            self.on_render()

        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()