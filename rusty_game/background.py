import re
import pygame
from log import Logerer
from colours import *
from time import sleep
from numpy import add

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
        self.blocks = set()
        self.liquid = set()
        self.level_lines = []
        self.block_width = 0
        self.block_height = 0
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
        self.block_vectors = (self.block_width ,self.block_height)
        self.get_npcs()

    def dummy(self, *args):
        pass

    def log(self, message):
        '''basic logging method'''
        if self.verbose:
            self.logger.log(__name__ + " : " + self.name, message)
    
    def listify(self, a_string):
        return a_string.replace(" ","").split(",")

    def get_npcs(self):
        self.npc_names = self.meta.get("npcs", False)
        if not self.npc_names:
           self.log("No npcs")
           self.npcs = False
           return False
        self.npc_names = self.listify(self.npc_names)
        self.npcs = {}
        for name in self.npc_names:
           self.npcs[name] = {"position" : self.meta.get(name + ".position", "0, 4")}
           self.npcs[name]["position"] = self.listify(self.npcs[name]["position"])
        self.log(str(self.npcs))
  
    def draw_block_background(self, block_string, x, y):
        '''takes the block string and the x y coordinates'''
        self.block_matrix.get(block_string, self.dummy)(x, y)

    def draw_block_foreground(self, block_string, x, y):
        '''intended to run and draw foreground elements'''

    def draw_block_colour(self, x, y, colour, corners=[True, True, True, True]):
        '''draws a solid background colour at particular co-ordinates'''
        corners = list(corners)
        top_left = [x * self.hs, y * self.vs, self.hs/2, self.vs/2]
        top_right = [x * self.hs + self.hs/2, y * self.vs, self.hs/2 + 1, self.vs/2]
        bottom_left = [x * self.hs, y * self.vs + self.vs/2, self.hs/2, self.vs/2]
        bottom_right = [x * self.hs + self.hs/2, y * self.vs + self.vs/2, self.hs/2 + 1, self.vs/2]
        for corner in (top_left, top_right, bottom_left, bottom_right):
           c = corners.pop(0)
           if c:
              corner = add([1,1,1,1],corner)
              self.screen.fill(colour, corner)


    def draw_house(self, x, y):
        '''draws a house'''
        for X in x, x + 1:
           self.blocks.add((X, y))
        self.draw_block_colour(x, y, YELLOW, corners=[0,1,0,1])
        self.draw_block_colour(x + 1, y, YELLOW, corners=[1,0,1,0])
        

    def draw_water(self, x, y):
        '''draws water'''
        left = (x -1, y ) in self.liquid
        up = (x, y -1) in self.liquid
        self.liquid.add((x,y))
        if left:
           self.draw_block_colour(x, y, BLUE, corners=[0,0,1,0])
           left = True
        if up:
           self.draw_block_colour(x, y, BLUE, corners=[0,1,0,0])
           up = True
        if left and up:
           self.draw_block_colour(x, y, BLUE, corners=[1,0,0,0])
        self.draw_block_colour(x, y, BLUE, corners=[0,0,0,1])

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
npcs= Ian, Keith
Keith.position=4, 0
             [ h ]
             [ ~ ]
             [ # ]'''
    my_background = Background("one", level)
    while True:
        my_background.draw_level(50, 50)
        pygame.display.update()
