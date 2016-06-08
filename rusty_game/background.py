import re

from log import Logerer
from colours import *

class Background(object):
  '''class to draw background given a string''' 
  
  def __init__(self, name, level_string, verbose=True):
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
     self.block_matrix = {"h": self.draw_house,
                          "~": self.draw_water,
                          "#": self.draw_path}

     for line in self.level_string.split("\n"):
        if "=" in line:
           key, value = line.split("=")
           self.meta[key] = value
        if "[" in line and "]" in line:
           match = re.match(".*\[(.*)\]" , line)
           self.level_lines.append(match.group(1))
           self.block_height += 1
           if len(match.group(1)) > self.block_width:
              self.block_width = len(match.group(1))

  def log(self, message):
     '''basic logging method'''
     if self.verbose:
        self.logger.log(__name__ + ":" + self.name, message)

  def draw_block_background(self, name, x, y):
     self.log(name + str(x) + str(y) + "-back")
  
  def draw_block_foreground(self, name, x, y):
     self.log(name + str(x) + str(y) + "-fore")
       
  def draw_house(self):
     pass

  def draw_water(self):
     pass

  def draw_path(self):
     pass
    
  def base_grass_biom(self):
     self.log("colour green")
     

  def draw_level(self, width, height, biom="grass"):
     self.scalar = (self.horizontal_scalar, self.vertical_scalar) = (self.hs,self.vs) = (width / self.block_width , height / self.block_width) 
     y = 0
     x = 0
     if biom=="grass":
        self.base_grass_biom()
     for line in self.level_lines:
        for block in line:
           self.draw_block_background(block, x, y)
           self.draw_block_foreground(block, x, y)
           x += 1
        y += 1
        x=0
        
         
     


if __name__ == '__main__':
  level = '''meta=test
             [ h ]
             [ ~ ]
             [ # ]'''
  my_background = Background("one", level)
  while True:
     my_background.draw_level(50, 50)

