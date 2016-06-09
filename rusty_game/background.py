import re
import pygame
from log import Logerer
from colours import *


class Background(object):
    '''class to draw background given a string'''

    def __init__(self, name, level_string, verbose=True, screen=False):
        '''class for creating background'''
        self.name = name
        self.level_string = level_string
        self.verbose = verbose
        self.logger = Logerer()
        self.log(level_string)
        self.meta = {}
        self.level_lines = []
        self.block_width = 0
        self.block_height = 0
        self.impassable_blocks = set()
        self.block_matrix = {"h": self.draw_house,
                             "~": self.draw_water,
                             "#": self.draw_path}
        self.screen = pygame.display.set_mode(
            (50, 50), pygame.RESIZABLE) if not screen else screen

        for line in self.level_string.split("\n"):
            if "=" in line:
                key, value = line.split("=")
                self.meta[key] = value
            if "[" in line and "]" in line:
                match = re.match(".*\[(.*)\]", line)
                self.level_lines.append(match.group(1))
                self.block_height += 1
                if len(match.group(1)) > self.block_width:
                    self.block_width = len(match.group(1))

    def dummy(*args):
        pass

    def log(self, message):
        '''basic logging method'''
        if self.verbose:
            self.logger.log(__name__ + ":" + self.name, message)

    def draw_block_background(self, block_string, x, y):
        '''takes the block string and the x y coordinates'''
        #self.log(block_string + str(x) + str(y) + "-back")
        self.block_matrix.get(block_string, self.dummy)(x, y)

    def draw_block_foreground(self, block_string, x, y):
        '''intended to run and draw foreground elements'''
        #self.log(block_string + str(x) + str(y) + "-fore")

    def draw_block_colour(self, x, y, colour):
        '''draws a solid background colour at particular co-ordinates'''
        rect = [x * self.hs, y * self.vs, self.hs, self.vs]
        self.screen.fill(colour, rect)

    def draw_house(self, x, y):
        '''draws a house'''
        self.draw_block_colour(x, y, YELLOW)

    def draw_water(self, x, y):
        '''draws water'''
        self.draw_block_colour(x, y, BLUE)

    def draw_path(self, x, y):
        '''draws a path'''
        self.draw_block_colour(x, y, WHITE)

    def base_grass_biom(self):
        '''draws a default grass biom'''
        #self.log("colour green")
        self.screen.fill(GREEN)

    def draw_level(self, width, height, biom="grass"):
        '''sets scalars for other drawing methods and '''
        self.scalar = (self.horizontal_scalar, self.vertical_scalar) = (
            self.hs, self.vs) = (width / self.block_width, height / self.block_width)
        y = 0
        x = 0
        if biom == "grass":
            self.base_grass_biom()
        for line in self.level_lines:
            for block in line:
                if block is not " ":
                    self.draw_block_background(block, x, y)
                    self.draw_block_foreground(block, x, y)
                x += 1
            y += 1
            x = 0


if __name__ == '__main__':
    pygame.init()
    level = '''meta=test
             [ h ]
             [ ~ ]
             [ # ]'''
    my_background = Background("one", level)
    while True:
        my_background.draw_level(50, 50)
