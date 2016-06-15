import pygame
import os
from random import choice
from numpy import add
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
        self.log("Game started in " + self.path)
        self.levels = {}
        self.current_level = (0, 0)
        self.width = width
        self.height = height
        self.size = self.width, self.height
        self.slow_clock = 90
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
            level_tup = tuple([int(string)
                               for string in level.replace('.lvl', '').split('-')])
            self.levels[level_tup] = Background(
                level, level_string=level_string, screen=self.screen, verbose=self.verbose)

    def load_main_character(self):
        self.main_character = Character(
            "Dave", screen=self.screen, verbose=self.verbose)

    def load_npcs(self):
        self.npcs = {}
        if self.levels[self.current_level].npcs and not self.npcs_loaded:
            npcs = self.levels[self.current_level].npcs
            for npc in npcs:
                position = npcs[npc]["position"]
                position = [int(v) for v in position]
                self.npcs[npc] = NPC(
                    npc, screen=self.screen, position=position, verbose=self.verbose)
                self.log(str(self.npcs[npc]))
            self.npcs_loaded = True
        return True

    def main(self):
        self.load_levels()
        self.load_main_character()
        self.load_new_level(self.current_level)
        self.clock = pygame.time.Clock()
        self.loop()

    def handle_size(self):
        self.width, self.height = self.controls.get_events(
            events=self.events, screen=self.screen, width=self.width, height=self.height, character=self.main_character)
        if self.size != (self.width, self.height):
            self.log(str((self.width, self.height)))
            self.screen = pygame.display.set_mode(
                (self.width, self.height), pygame.RESIZABLE)

    def load_new_level(self, level_name):
        self.blocks = self.levels[level_name].blocks
        self.liquid = self.levels[level_name].liquid
        self.current_level = level_name
        self.load_npcs()

    def next_level(self, vector, direction):
        self.log(str(vector) + " going " + str(direction))
        change = [0, 0]
        change[vector] = direction
        new_level = tuple(add(self.current_level, change))
        if self.levels.get(new_level, False):
            self.npcs_loaded = False
            self.load_new_level(new_level)
            if self.main_character.position[vector] < 0:
                self.main_character.position[vector] = self.levels[
                    self.current_level].block_vectors[vector]
            else:
                self.main_character.position[vector] = 0
        else:
            self.log("level " + str(new_level) + " not available")

    def handle_npcs(self):
        for char in self.npcs:
            self.npcs[char].blocks = set(self.temp_blocks)
            if not self.npcs[char].can_swim:
                self.npcs[char].blocks.update(self.liquid)
            self.npcs[char].draw_character(
                self.levels[self.current_level].hs, self.levels[self.current_level].vs)
            self.temp_blocks.add(tuple(self.npcs[char].position))
            if self.counter == self.slow_clock:
                choice((self.npcs[char].dummy, self.npcs[char].move_rand))()

    def handle_character_position(self):
        for vector in range(2):
            if self.main_character.position[vector] > self.levels[self.current_level].block_vectors[vector]:
                self.next_level(vector, +1)
            elif self.main_character.position[vector] < 0:
                self.next_level(vector, -1)

    def loop(self):
        self.counter = 0
        while True:
            self.temp_blocks = set(self.blocks)
            self.size = self.width, self.height
            self.events = pygame.event.get()
            self.handle_size()
            self.levels[self.current_level].draw_level(self.width, self.height)
            self.main_character.draw_character(
                self.levels[self.current_level].hs, self.levels[self.current_level].vs)
            self.temp_blocks.add(tuple(self.main_character.position))
            if self.levels[self.current_level].npcs:
                self.handle_npcs()
            self.main_character.blocks = self.temp_blocks
            if not self.main_character.can_swim:
                print "main character can't swim"
                self.main_character.blocks.update(self.liquid)
            self.handle_character_position()
            self.clock.tick(60)
            pygame.display.update()
            self.clock.tick(60)
            if self.counter == self.slow_clock:
                self.counter = 0
            self.counter += 1

def main():
    main_game = Game()
    main_game.main()

if __name__ == '__main__':
    main()
