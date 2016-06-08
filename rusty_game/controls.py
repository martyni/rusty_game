import os
import pygame
from collections import namedtuple
from yaml import load, dump
from log import Logerer
path = os.path.dirname(__file__) if os.path.dirname(__file__) else False

try:
   from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
   from yaml import Loader, Dumper


class Controls(object):
   def __init__(self, path=path, verbose=True):
      self.path = path
      self.settings = path + "/static/controls.yaml" if path else "static/controls.yaml"
      self.control_dict = load(open(self.settings,"r").read())
      self.control_lookup = { self.control_dict[key]:key for key in self.control_dict }
      self.verbose = verbose
      self.logger = Logerer()
      self.direction = {key:False for key in self.control_dict}

   def log(self, message):
      if self.verbose:
         self.logger.log(__name__, message)
          
   def get_events(self, events, screen, width, height):
      for e in events:
         if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 5:
               self.log("scroll in")
            elif e.button == 4:
               self.log("scroll out")
         if e.type == pygame.QUIT:
            self.log("quit")
            quit()
         if e.type == pygame.VIDEORESIZE:
            self.log("resize {}".format(str(e.size)))
            width, height = e.size
         if e.type == pygame.KEYDOWN:   
            key = self.control_lookup.get(e.key, False)
            if key:
               self.direction[key] = True 
               self.log(self.direction)
         elif e.type == pygame.KEYUP:
            key = self.control_lookup.get(e.key, False)
            if key:
               self.direction[key] = False
               self.log(self.direction)
               self.events = events
      return width, height  

if __name__ == "__main__":
   my_controls = Controls()
   pygame.init()
   width = 50
   height = 50
   screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
   while True:  
      width,height = my_controls.get_events(pygame.event.get(), screen, width, height)  
