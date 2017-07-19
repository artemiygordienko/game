# -*- coding: utf-8 -*-
import pygame, sys
#from main import *

WIN_WIDTH = 800
WIN_HEIGHT = 600
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)

screen = pygame.display.set_mode(DISPLAY)
class Menu:
    def __init__(self, items=[400, 350, u'Item', (250, 250, 30), (250, 30, 250)]):
        self.items = items

    def render(self, side, font, num_item):
        for i in self.items:
            if num_item == i[5]:
                side.blit(font.render(i[2], 1, i[4]), (i[0], i[1] - 30))
            else:
                side.blit(font.render(i[2], 1, i[3]), (i[0], i[1] - 30))

    def menu(self):
        done = True
        font_menu = pygame.font.Font('fonts/Shumi.otf', 50)
        pygame.key.set_repeat(0, 0)
        pygame.mouse.set_visible(True)
        item = 0
        while done:
            screen.fill((0, 100, 200))
            """Делаем возможность выбора курсором мыши"""
            mp = pygame.mouse.get_pos()
            for i in self.items:
                if mp[0] > i[0] and mp[0] < i[0] + 155 and mp[1] > i[1] and mp[1] < i[1] + 50:
                    item = i[5]
            self.render(screen, font_menu, item)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        sys.exit()
                    if e.key == pygame.K_UP:
                        if item > 0:
                            item -= 1
                    if e.key == pygame.K_DOWN:
                        if item < len(self.items) - 1:
                            item += 1
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if item == 0:
                        done = False
                    elif item == 1:
                        exit()
            screen.blit(screen, (0, 30))
            pygame.display.flip()