import pygame
import os
from controls import Controls
from background import Background
from log import Logerer
from character import Character
from colours import *

WIDTH = 100
HEIGHT = 100


class Game(object):

    def __init__(self, verbose=True, path=False, width=WIDTH, height=HEIGHT):
        self.controls = Controls(verbose=False)
        self.logger = Logerer()
        self.path = self.controls.path if not path else path
        self.verbose = verbose
        self.log("Game started")
        self.levels = {}
        self.current_level = '0-0'
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.RESIZABLE)

    def log(self, message):
        if self.verbose:
            self.logger.log(__name__, message)

    def load_levels(self):
        suffix = '/static/levels/'
        levels = [f for f in os.walk(self.path + suffix)][0][2]
        print levels
        for level in levels:
            self.log(level + " loaded")
            level_path = self.path + suffix + level
            level_string = open(level_path, 'r').read()
            self.levels[level.replace('.lvl', '')] = Background(
                level, level_string=level_string, screen=self.screen, verbose=False)

    def load_main_character(self):
        self.main_character = Character("Dave", screen=self.screen)

    def main(self):
        self.load_levels()
        self.load_main_character()
        self.clock = pygame.time.Clock()
        self.loop()

    def loop(self):
        while True:
            self.size = self.width, self.height
            self.events = pygame.event.get()
            self.width, self.height = self.controls.get_events(
                events=self.events, screen=self.screen, width=self.width, height=self.height, character=self.main_character)
            if self.size != (self.width, self.height):
                self.log(str((self.width, self.height)))
                self.screen = pygame.display.set_mode(
                    (self.width, self.height), pygame.RESIZABLE)
            self.levels[self.current_level].draw_level(self.width, self.height)
            self.main_character.draw_character(self.levels[self.current_level].hs, self.levels[self.current_level].vs)
            pygame.display.update()
            self.clock.tick(60)


def main():
    main_game = Game()
    main_game.main()

if __name__ == '__main__':
    main()
