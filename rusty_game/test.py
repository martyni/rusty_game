import pygame
import re
import unittest

from log import Logerer
from controls import Controls
from background import Background
from colours import *

pygame.init()



level_string = '''meta=test
                  [ h ]
                  [ ~ ]
                  [ # ]'''

class TestLogerer(unittest.TestCase):

   def test_log(self):
      '''Checks log formatting'''
      test_logerer = Logerer()
      log = test_logerer.log("test", "testing logging")
      self.assertTrue(re.match("[0-1][0-9]:[0-5][0-9]:[0-5][0-9] [0-3][0-9]/[0-1][0-9]/[0-9][0-9]-test : testing logging", log) )


class TestControls(unittest.TestCase):

   def test_controls(self):
      '''Fake some key ups and key downs then check that changes control booleans'''
      self.screen = pygame.display.set_mode((50, 50), pygame.RESIZABLE)
      test_controls = Controls(path='test_static', verbose=False)

      events = [pygame.event.Event(pygame.KEYDOWN, key=control, mod=4096) for control in test_controls.control_lookup]
      test_controls.get_events(events, self.screen)
      for key in test_controls.direction:
         self.assertTrue(test_controls.direction[key]) 

      events = [pygame.event.Event(pygame.KEYUP, key=control, mod=4096) for control in test_controls.control_lookup]   
      test_controls.get_events(events, self.screen)
      for key in test_controls.direction:
         self.assertFalse(test_controls.direction[key])
   
class TestBackground(unittest.TestCase):
                   
   def create(self, name, level_string):
       '''basic method for creating backgrounds'''
       return Background(name, level_string, verbose=False)

   def test_meta(self):
       '''checking meta data is loaded'''
       meta_background = self.create("meta", level_string)
       self.assertEqual(meta_background.meta.get("meta", False), "test")  

   def test_height(self):
       '''checking height is properly set'''
       meta_background = self.create("height", level_string)
       self.assertEqual(meta_background.block_height, 3)

   def test_width(self):
       '''checking width is properly set'''
       meta_background = self.create("width", level_string)
       self.assertEqual(meta_background.block_width, 3)
 
   def test_level(self):
       '''checking level is properly set'''
       meta_background = self.create("level", level_string)
       self.assertEqual(meta_background.level_lines[0], " h ")

   def test_scalars(self):
       '''Checking scalar value works'''
       meta_background = self.create("scalar", level_string)
       meta_background.draw_level(60, 120)
       self.assertEqual(meta_background.horizontal_scalar, 20)
       self.assertEqual(meta_background.vertical_scalar, 40)

if __name__ == '__main__':
    unittest.main()
