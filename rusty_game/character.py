import pygame
from random import choice
from time import sleep
from log import Logerer
from colours import *


class Character(object):
    colour = DARK_YELLOW
    lower_limit = [-2, -2]
    upper_limit = [15, 14]
    can_swim = False
    def __init__(self, name, screen=False, verbose=True, position=[0, 0]):
        self.name = name
        self.logger = Logerer()
        self.verbose = verbose
        self.position = position
        self.speed = [10, 10]
        self.buttons = {}
        self.blocks = set([1])
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

    def dummy(self, *args, **kwargs):
        pass

    def log(self, message):
        if self.verbose:
            self.logger.log(__name__ + " : " + self.name, message)

    def draw_character(self, hs, vs):
        '''Draws character once per frame'''
        # hs and vs short for horizontal scalar and vertical scalar respectivly
        self.hs = hs
        self.vs = vs
        self.scalars = self.hs, self.vs
        rect = (self.hs/4 + self.position[0] * self.hs + self.move_vectors[0],
                self.vs/4 + self.position[1] * self.vs + self.move_vectors[1], hs/2, vs/2)
        pygame.draw.ellipse(self.screen, self.colour, rect)
        # for horizontal and vertical axis check if move_vector have reached
        # zero if they haven't add/subtract the appropriate scalar /speed
        for vector in range(2):
            if self.move_vectors[vector] > 0:
                if self.move_vectors[vector] <= self.scalars[vector] / self.speed[vector]:
                   self.move_vectors[vector] = 0
                else:
                   self.move_vectors[
                       vector] -= (self.scalars[vector] / self.speed[vector])
                
            elif self.move_vectors[vector] < 0:
                if self.move_vectors[vector] >= -self.scalars[vector] / self.speed[vector]:
                   self.move_vectors[vector] = 0
                else:
                   self.move_vectors[
                       vector] += (self.scalars[vector] / self.speed[vector])
            elif self.move_vectors[vector] == 0:
                self.vector_is_pressed(vector)

    def vector_is_pressed(self, vector):
        '''Called when move_vectors reach zero '''
        directions = (self.last_pressed[1], "up", "down") if vector else (self.last_pressed[0], "left", "right")
        for direction in directions:
            if self.buttons.get(direction, False):
                self.move_matrix[direction]()
                return None

    def check_sqaure_empty(self, vector, direction):
        self.test_position = list(self.position)
        self.test_position[vector] += direction
        return True if tuple(self.test_position) not in self.blocks else False
        
    def go(self, vector, amount, direction):
        if self.upper_limit[vector] > self.position[vector] + direction > self.lower_limit[vector]:
            if self.check_sqaure_empty(vector, direction):
                self.position[vector] += direction
                self.move_vectors[vector] = amount
            else:
                self.log("square is occupied " + str(self.test_position))
                return None
        elif self.upper_limit[vector] > self.position[vector] + direction:
           self.log("lower boundary")
           return None
        elif self.upper_limit[vector] < self.position[vector] + direction:
           self.log("upper boundary")
           return None
        log_message = "moving to " + str(self.position) + ": scalar is " + str(amount) + ": step size is " + str(self.scalars[
            vector] / self.speed[vector]) + ": (x, y) co-ordinates " + str((self.hs * self.position[0], self.vs * self.position[1]))
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

class NPC(Character):
    colour = DARK_RED
    lower_limit = [-1, -1]
    upper_limit = [13, 13]
    can_swim = False

    def move_rand(self):
       choice((self.move_down, self.move_up, self.move_left, self.move_right, self.dummy))()
    

if __name__ == "__main__":
    pygame.init()
    dave = Character("Dave")
    dave.draw_character(50, 50)
    pygame.display.update()
    for direction in [dave.move_right, dave.move_down, dave.move_left, dave.move_up]:
        direction()
        for i in range(dave.speed[0]):
            dave.screen.fill(BLACK)
            dave.draw_character(50, 50)
            sleep(0.1)
            pygame.display.update()
