import pygame
from log import Logerer
from colours import *


class Character(object):

    def __init__(self, name, screen=False, verbose=True, position=[0, 0]):
        self.name = name
        self.logger = Logerer()
        self.verbose = verbose
        self.position = position
        self.speed = [5, 5]
        self.buttons = {}
        self.move_vectors = [0, 0]
        self.last_pressed = [False, False]
        self.screen = pygame.display.set_mode(
            (50, 50), pygame.RESIZABLE) if not screen else screen
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
        self.vs = vs
        self.hs = hs
        self.scalars = self.hs, self.vs
        rect = (self.position[0] * self.hs + self.move_vectors[0],
                self.position[1] * self.vs + self.move_vectors[1], hs, vs)
        pygame.draw.ellipse(self.screen, BLACK, rect)
        for direction in range(2):
            if self.move_vectors[direction] > 0:
                self.move_vectors[direction] -= (self.scalars[direction] / self.speed[direction])
            elif self.move_vectors[direction] < 0:
                self.move_vectors[direction] += (self.scalars[direction] /  self.speed[direction])
            elif self.move_vectors[direction] == 0:
                self.direction_is_pressed(direction)
                


    def direction_is_pressed(self, vector):
        directions = ("up", "down") if vector else ("left", "right")
        for direction in directions:
            if self.buttons.get(direction, False) and directions == self.last_pressed[vector]:
                self.move_matrix[direction]()
                return None
            elif self.buttons.get(direction, False):
                self.move_matrix[direction]()
                return None

    def go(self, direction, amount, position):
        self.move_vectors[direction] = amount
        self.position[direction] += position
        if amount > 0:
           self.log("deducted " + str((self.scalars[direction] % self.speed[direction])))
           self.move_vectors[direction] -= (self.scalars[direction] % self.speed[direction])
        else:
           self.log("added " + str((self.scalars[direction] % self.speed[direction])))
           self.move_vectors[direction] += (self.scalars[direction] % self.speed[direction])

        log_message = "moving to " + str(self.position) + " scalar is " + str(amount)
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
