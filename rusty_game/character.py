import pygame
from time import sleep
from log import Logerer
from colours import *

class Character(object):

    def __init__(self, name, screen=False, verbose=True, position=[0, 0]):
        self.name = name
        self.logger = Logerer()
        self.verbose = verbose
        self.position = position
        self.speed = [10, 10]
        self.buttons = {}
        self.move_vectors = [0, 0]
        self.last_pressed = [False, False]
        self.screen = pygame.display.set_mode(
            (100, 100), pygame.RESIZABLE) if not screen else screen
        self.opposites = {"up": "down",
                          "down": "up",
                          "left": "right",
                          "right": "left"}
        self.move_matrix = {"up": self.move_up,
                            "down": self.move_down,
                            "left": self.move_left,
                            "right": self.move_right}

    def dummy(self, args):
        pass

    def log(self, message):
        if self.verbose:
            self.logger.log(self.name, message)

    def draw_character(self, hs, vs):
        '''Draws character once per frame'''
        self.vs = vs
        self.hs = hs
        self.scalars = self.hs, self.vs
        rect = (self.position[0] * self.hs + self.move_vectors[0],
                self.position[1] * self.vs + self.move_vectors[1], hs, vs)
        pygame.draw.ellipse(self.screen, DARK_YELLOW, rect)
        for vector in range(2):
            if self.move_vectors[vector] > 0:
                self.move_vectors[vector] -= (self.scalars[vector] / self.speed[vector])
            elif self.move_vectors[vector] < 0:
                self.move_vectors[vector] += (self.scalars[vector] /  self.speed[vector])
            elif self.move_vectors[vector] == 0:
                self.vector_is_pressed(vector)
                


    def vector_is_pressed(self, vector):
        '''Called when move_vectors reach zero '''
        directions = ("up", "down") if vector else ("left", "right")
        for direction in directions:
            if self.buttons.get(direction, False) and directions == self.last_pressed[vector]:
                self.move_matrix[direction]()
                return None
            elif self.buttons.get(direction, False):
                self.move_matrix[direction]()
                return None

    def go(self, vector, amount, position):
        self.move_vectors[vector] = amount
        self.position[vector] += position
        #Hack to make sure that move_vectors reach zero by taking the modulus out 
        if amount > 0:
           self.move_vectors[vector] -= (self.scalars[vector] % self.speed[vector])
        else:
           self.move_vectors[vector] += (self.scalars[vector] % self.speed[vector])
        log_message = "moving to " + str(self.position) + " scalar is " + str(amount) + " step size is " + str(self.scalars[vector] / self.speed[vector])
        self.log(log_message)

    def move_up(self):
        self.last_pressed[1] = "up"
        self.go(1, self.vs, -1)

    def move_down(self):
        self.last_pressed[1] = "down"
        self.go(1, -self.vs, +1)

    def move_left(self):
        self.last_pressed[0] = "left"
        self.go(0, self.hs, -1)

    def move_right(self):
        self.last_pressed[0] = "right"
        self.go(0, -self.hs, +1)

if __name__ == "__main__":
   pygame.init()
   dave = Character("Dave")
   dave.draw_character(50,50)
   pygame.display.update()
   for direction in [dave.move_right, dave.move_down, dave.move_left, dave.move_up]:
      direction()
      for i in range(dave.speed[0]):
         dave.screen.fill(BLACK)
         dave.draw_character(50,50)
         sleep(0.1)
         pygame.display.update()
