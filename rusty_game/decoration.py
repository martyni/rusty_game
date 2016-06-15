import pygame
from pygame import gfxdraw
from time import sleep
from colours import *
from numpy import add

class Decoration(object):
    def __init__(self, screen=False, h_scalar=200, v_scalar=200, special=False):
        self.screen = pygame.display.set_mode(
                   (1500, 1500), pygame.RESIZABLE) if not screen else screen
        self.hs = h_scalar
        self.vs = v_scalar
        self.special = special

    def lighten(self, colour, amount=2):
        col_list = []
        for each in colour:
           new_colour = each * amount if each * amount < 255 else 255
           col_list.append(new_colour)
        return tuple(col_list)

    def darken(self, colour, amount=3):
        col_list = []
        for each in colour[:3:]:
           if each:
              new_colour = each / amount
           col_list.append(new_colour)
        col_list.append(255)
        return tuple(col_list)

    def draw_shape(self, points, colour):
        pygame.draw.polygon(self.screen, colour, points)
        pygame.draw.aalines(self.screen, BLACK, True, points)
 
    def draw_hair(self, x, y, colour):
        points = [(x,y - self.vs/6),
                  (x - self.hs/4, y),
                  (x - self.hs/2, y),
                  (x - self.hs/4, y + self.vs/10),
                  (x + self.hs/4, y + self.vs/10),
                  (x + self.hs/2, y),
                  (x + self.hs/4, y),
                 ]
        self.draw_shape(points, colour)

    def draw_fringe(self, x, y, colour):
        hairs = 6
        for i in range(-hairs +1, hairs, 2):
           X = x + i * self.hs/hairs/5
           self.draw_shape([(X, y -self.vs/30), (X -self.hs/20, y - self.vs/7), (X + self.hs/20, y - self.vs/7)], colour)
        

    def draw_rect(self, x, y, colour):
        points = [(x * self.hs, y * self.vs),
                 ((x + 1 )* self.hs, y * self.vs),
                 ((x + 1 )* self.hs, (y + 1) * self.vs),
                 (x * self.hs, (y + 1) * self.vs)]
        self.draw_shape(points, colour)

    def draw_triangle(self, x, y, colour):
        points = [((x + 0.5) * self.hs, y * self.vs),
                  (x  * self.hs, (y + 1) * self.vs),  
                  ((x + 1)  * self.hs, (y + 1) * self.vs)]
        self.draw_shape(points, colour)  

    def draw_circle(self, x, y, colour):
        gfxdraw.filled_ellipse(self.screen, int((x + 0.5) * self.hs), int((y + 0.5) * self.vs), self.hs/2, self.vs/2, colour)
        gfxdraw.aaellipse(self.screen, int((x + 0.5) * self.hs), int((y + 0.5) * self.vs), self.hs/2, self.vs/2, BLACK)
     
    def draw_pie(self, x, y, colour, angle, size, x_offset=0, y_offset=0):
        gfxdraw.pie(self.screen, 
                    x + x_offset, 
                    y + y_offset, 
                    self.vs/2,
                    angle -size,
                    angle +size, 
                    colour) 
    
    def step(self, x, y, step, colour):
        step += 1
        if step >= 8:
           step = step % 8
        right_leg = [90, 100, 110, 120, 125, 125,  120, 110, 100, 90]
        left_leg =  [90, 80,  70,  60,  55,  55,   60,  70,  80,  90]
        limit = 10
        for i in range(limit):
           self.draw_pie(x, y, colour, right_leg[step], i)
           self.draw_pie(x, y, colour, left_leg[step], i)

        for i in (limit - 2, limit - 1, limit, limit + 1):
           self.draw_pie(x, y, BLACK, right_leg[step], i)
           self.draw_pie(x, y, BLACK, left_leg[step], i)

    def draw_arm(self, x, y, step, colour, front=True):
        if front:
           sequence = [90] + range(50, 131,10)
           sequence += sequence[::-1]
        else:
           sequence = [90] + range(130,49,-10)
           sequence += sequence[::-1]
        if step >= 9:
           step = step % 10

        self.draw_pie(x, y, colour, sequence[step], 0, y_offset=-self.vs/5)
        self.draw_pie(x, y, BLACK, sequence[step], 2, y_offset=-self.vs/5)

    def draw_person(self, x, y, step, colour):
        step = abs(step)
        dark_colour = self.darken(colour)
        light_colour = self.lighten(colour, amount=20)
        self.step(x, y, step, dark_colour)
        #back arm
        self.draw_arm(x, y, step, colour, front=False)
        #body
        gfxdraw.filled_ellipse(self.screen, x, y, self.hs/8, self.vs/4, colour)
        gfxdraw.aaellipse(self.screen, x, y, self.hs/8, self.vs/4, BLACK)
        #head
        if self.special:
           self.draw_hair(x, y - self.vs/3,colour)
        gfxdraw.filled_ellipse(self.screen, x, y - self.vs/3, self.hs/4, self.vs/7, light_colour)
        gfxdraw.aaellipse(self.screen, x, y - self.vs/3, self.hs/4, self.vs/7, BLACK)

        #creepy eyes 
        gfxdraw.filled_ellipse(self.screen, x - self.hs/10, y - self.vs/3, self.hs/15, self.vs/15, WHITE)
        gfxdraw.aaellipse(self.screen, x - self.hs/10, y - self.vs/3, self.hs/15, self.vs/15, BLACK)
        gfxdraw.filled_ellipse(self.screen, x - self.hs/10, y - self.vs/3, self.hs/35, self.vs/35, BLACK)
        gfxdraw.filled_ellipse(self.screen, x + self.hs/10, y - self.vs/3, self.hs/15, self.vs/15, WHITE)
        gfxdraw.aaellipse(self.screen, x + self.hs/10, y - self.vs/3, self.hs/15, self.vs/15, BLACK)
        gfxdraw.filled_ellipse(self.screen, x + self.hs/10, y - self.vs/3, self.hs/35, self.vs/35, BLACK)

        self.draw_fringe(x, y - self.vs/3, colour)
        #front arm
        self.draw_arm(x, y, step, colour)
    

if __name__ == "__main__":
   dec = Decoration()
   dec.screen.fill(WHITE)
   dec.draw_rect(1, 1, YELLOW)
   dec.draw_triangle(1, 0, RED)
   dec.draw_circle(1, 2, BLUE)
   pygame.display.update()
   sleep(0.5)

   for i in range(20):
      dec.screen.fill(WHITE)
      dec.draw_person(dec.hs/2 + int(i/10.0 * dec.hs),dec.vs/2, i, RED)
      sleep(0.05)
      pygame.display.update()

   for i in range(20):
      dec.screen.fill(WHITE)
      dec.draw_person(int(2.5 * dec.hs), dec.vs/2 + int(i/10.0 * dec.vs), i, BLUE)
      sleep(0.05)
      pygame.display.update()
   dec.draw_fringe(dec.hs/4, dec.vs/5, BLUE)
   pygame.display.update()
   sleep(5)
