import pygame
import re
import unittest
from time import sleep
from log import Logerer
from controls import Controls
from background import Background
from character import Character
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
        self.assertTrue(re.match(
            "[0-1][0-9]:[0-5][0-9]:[0-5][0-9] [0-3][0-9]/[0-1][0-9]/[0-9][0-9] test : testing logging", log))


class TestControls(unittest.TestCase):

    def test_controls(self):
        '''Fake some key ups and key downs then check that changes control booleans'''
        self.screen = pygame.display.set_mode((50, 50), pygame.RESIZABLE)
        test_controls = Controls(verbose=False)
        test_controls.path = test_controls.path.replace(
            'static', 'test/static')
        events = [pygame.event.Event(pygame.KEYDOWN, key=control, mod=4096)
                  for control in test_controls.control_lookup]
        test_controls.get_events(events, self.screen, 50, 50)
        for key in test_controls.buttons:
            self.assertTrue(test_controls.buttons[key])

        events = [pygame.event.Event(pygame.KEYUP, key=control, mod=4096)
                  for control in test_controls.control_lookup]
        test_controls.get_events(events, self.screen, 50, 50)
        for key in test_controls.buttons:
            self.assertFalse(test_controls.buttons[key])

        
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

    def test_house(self):
        house = self.create('house', '[h]')
        house.draw_level(50, 50)
        self.assertEqual(house.screen.get_at((4, 4)), YELLOW)

    def test_default(self):
        house = self.create('default', '[ ]')
        house.draw_level(50, 50)
        self.assertEqual(house.screen.get_at((0, 0)), GREEN)

    def test_water(self):
        house = self.create('water', '[~]')
        house.draw_level(50, 50)
        self.assertEqual(house.screen.get_at((0, 0)), BLUE)

    def test_path(self):
        house = self.create('path', '[#]')
        house.draw_level(50, 50)
        self.assertEqual(house.screen.get_at((0, 0)), WHITE)

class TestCharacter(unittest.TestCase):
    def create_character(self, name):
        '''basic character creation'''
        return Character(name, verbose=False)
    
    def test_draw_character(self):
        draw_character = self.create_character("draw")
        draw_character.draw_character(50, 50)
        self.assertEqual(draw_character.screen.get_at((25,25)), DARK_YELLOW)

    def test_move_character(self):
        draw_character = self.create_character("draw")
        draw_character.draw_character(50, 50)
        self.assertEqual(draw_character.screen.get_at((25,25)), DARK_YELLOW)
        old_vectors = (25, 25)
        for direction, new_vectors in [(draw_character.move_right, (75, 25)),
                                       (draw_character.move_down, (75, 75)),
                                       (draw_character.move_left, (25, 75)), 
                                       (draw_character.move_up, (25,25))]: 
           direction()
           for frame in range(draw_character.speed[0]):
              #character takes speed frames to move character for tests horizontal and vertical speed are the same
              draw_character.screen.fill(BLACK)
              draw_character.draw_character(50, 50)
           self.assertEqual(draw_character.screen.get_at(old_vectors), BLACK)
           self.assertEqual(draw_character.screen.get_at(new_vectors), DARK_YELLOW)
           old_vectors = new_vectors


if __name__ == '__main__':
    unittest.main()
