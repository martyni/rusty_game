import pygame
import re
import unittest
import os
from time import sleep
from log import Logerer
from controls import Controls
from background import Background
from character import Character
from main import Game
from colours import *
path = os.path.dirname(__file__) if os.path.dirname(__file__) else False
pygame.init()
if path:
   path=path + "/test"
else:
   path = "test"

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

    def test_repeats(self):
        test_repeats = Logerer()
        test_repeats.log("test", "testing repeats")
        log = test_repeats.log("test", "testing repeats")
        self.assertFalse(log)

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
        house = self.create('house', '''[h ]
                                        [  ]''')
        house.draw_level(50, 50)
        pygame.display.update()
        self.assertEqual(house.screen.get_at((13, 0)), YELLOW)
        self.assertEqual(house.screen.get_at((20, 0)), YELLOW)

    def test_default(self):
        default = self.create('default', '[ ]')
        default.draw_level(50, 50)
        self.assertEqual(default.screen.get_at((0, 0)), GREEN)

    def test_water(self):
        water = self.create('water', '[~]')
        water.draw_level(50, 50)
        self.assertEqual(water.screen.get_at((25, 25)), BLUE)

    def test_water_left(self):
        water_left = self.create('water', '''[~~]
                                             [  ]''')
        water_left.draw_level(50, 50)
        self.assertEqual(water_left.screen.get_at((26, 12)), BLUE)
        
    def test_water_up(self):
        water_left = self.create('water', '''[~~]
                                             [~ ]''')
        water_left.draw_level(50, 50)
        self.assertEqual(water_left.screen.get_at((12, 26)), BLUE)

    def test_water_up_left(self):
        water_left = self.create('water', '''[~~]
                                             [~~]''')
        water_left.draw_level(50, 50)
        self.assertEqual(water_left.screen.get_at((26, 26)), BLUE)

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
              #character takes speed frames to move character for tests 
              draw_character.screen.fill(BLACK)
              draw_character.draw_character(50, 50)
           self.assertEqual(draw_character.screen.get_at(old_vectors), BLACK)
           self.assertEqual(draw_character.screen.get_at(new_vectors), DARK_YELLOW)
           old_vectors = new_vectors
    
class TestMain(unittest.TestCase):
    def create_game(self):
        return Game(verbose=False, path=path)

    def test_load_levels(self):
        levels = self.create_game()
        levels.load_levels()
        self.assertEqual(levels.levels[(0, 0)].level_string[0], "t")
        self.assertEqual(levels.levels[(0, 0)].meta["test"], "test")
    
    def test_load_main_character(self):
        character = self.create_game()
        character.load_main_character()
        self.assertEqual(character.main_character.name, "Dave")   
    
    def test_load_npcs(self):
        npcs = self.create_game()
        npcs.load_levels()
        npcs.load_npcs()
        self.assertEqual(npcs.npcs["test"].name, "test")

    def test_handle_size(self):
        size = self.create_game()
        size.load_main_character()
        #default size
        self.assertEqual(size.height, 522)
        size.events = [pygame.event.Event(pygame.RESIZABLE, h=500, w=500, size=(500, 500))]
        size.handle_size()
        self.assertEqual(size.height, 500)
        self.assertEqual(size.height, 500)
    
    def test_handle_character_position(self):
        char_pos = self.create_game()
        char_pos.load_main_character()
        char_pos.load_levels()
        self.assertEqual(char_pos.current_level, (0,0))
        char_pos.main_character.position = [15, 0]
        char_pos.handle_character_position()
        self.assertEqual(char_pos.current_level, (1,0))

if __name__ == '__main__':
    unittest.main()
