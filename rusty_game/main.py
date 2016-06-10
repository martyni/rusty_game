import pygame
import os
from random import choice
from controls import Controls
from background import Background
from log import Logerer
from character import Character, NPC
from colours import *

WIDTH = 480 
HEIGHT = 522


class Game(object):

    def __init__(self, verbose=True, path=False, width=WIDTH, height=HEIGHT):
        self.verbose = verbose
        self.logger = Logerer()
        self.controls = Controls(verbose=self.verbose)
        self.path = self.controls.path if not path else path
        self.log("Game started")
        self.levels = {}
        self.current_level = '0-0'
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.RESIZABLE)
        self.npcs_loaded = False

    def log(self, message):
        if self.verbose:
            self.logger.log(__name__, message)

    def load_levels(self):
        suffix = '/static/levels/'
        levels = [f for f in os.walk(self.path + suffix)][0][2]
        self.log(str(levels))
        for level in levels:
            self.log(level + " loaded")
            level_path = self.path + suffix + level
            level_string = open(level_path, 'r').read()
            self.levels[level.replace('.lvl', '')] = Background(
                level, level_string=level_string, screen=self.screen, verbose=self.verbose)
           
    def load_main_character(self):
        self.main_character = Character("Dave", screen=self.screen, verbose=self.verbose)
    
    def load_npcs(self):
        self.npcs = {}
        if self.levels[self.current_level].npcs and not self.npcs_loaded:
            npcs = self.levels[self.current_level].npcs
            for npc in npcs:
               position = npcs[npc]["position"]
               position = [int(v) for v in position]
               self.npcs[npc] = NPC(npc, screen=self.screen, position=position, verbose=self.verbose)
               self.log(str(self.npcs[npc]))
            self.npcs_loaded = True
        return True

    def main(self):
        self.load_levels()
        self.load_main_character()
        self.load_npcs()
        self.clock = pygame.time.Clock()
        self.loop()
    
    def handle_size(self):
        self.width, self.height = self.controls.get_events(
            events=self.events, screen=self.screen, width=self.width, height=self.height, character=self.main_character)
        if self.size != (self.width, self.height):
            self.log(str((self.width, self.height)))
            self.screen = pygame.display.set_mode(
                (self.width, self.height), pygame.RESIZABLE)

    def loop(self):
        counter = 0
        while True:
            self.size = self.width, self.height
            self.events = pygame.event.get()
            self.handle_size()
            self.levels[self.current_level].draw_level(self.width, self.height)
            self.main_character.draw_character(self.levels[self.current_level].hs, self.levels[self.current_level].vs)
            if self.levels[self.current_level].npcs:
               for char in self.npcs:
                  self.npcs[char].draw_character(self.levels[self.current_level].hs, self.levels[self.current_level].vs)
                  if counter == 100:
                     choice((self.npcs[char].dummy, self.npcs[char].move_rand))()
            
            pygame.display.update()
            self.clock.tick(60)
            if counter == 100:
               counter = 0
            counter +=1
def main():
    main_game = Game()
    main_game.main()

if __name__ == '__main__':
    main()
