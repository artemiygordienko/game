# -*- coding: utf-8 -*-

import pygame
from pygame import *
from player import *
from blocks import *
from mainmenu import *
from enemy import *


"""Создаем камеру"""


class Camera(object):
    """Камера будет перемещаться за персонажем"""

    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def main():
    pygame.init()  # Инициация PyGame, обязательная строчка
    pygame.font.init()  # Инициализация шрифтов
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("Platformer-1")  # Пишем в шапку
    bg = image.load("%s/backgr/backg.png" % ICON_DIR)  # загружаем картинку с фоном
    hero = Player(55, 55)  # создаем героя по (x,y) координатам
    monsters = pygame.sprite.Group()  # Все передвигающиеся объекты
    left = right = False  # по умолчанию - стоим
    up = False  # по умолчанию не прыгаем, если True, то скачет, как мяч
    running = False  # По умолчанию не ускоряется

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    entities.add(hero)

    level = [
        "----------------------------------",
        "-   -                            -",
        "-   -  *             ***--       -",
        "-   -         --------           -",
        "-   -            ***             -",
        "-   -                            -",
        "-   -                    **       -",
        "-   --              ----     --- -",
        "-   -    ---        --           -",
        "-   -****---        --           -",
        "-   -----           --           -",
        "-   -           ------       -------------------------",
        "-   -               --                               -",
        "-   -                ----              ****         ^-",
        "-   -                    **---------------------------",
        "-   -------  **                  -",
        "-   -           *-------         -",
        "-   -                            -",
        "-   -                     -      -",
        "-                            --  -",
        "-                                -",
        "-                               |-",
        "========**=***===================="]

    timer = pygame.time.Clock()
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "*":
                bd = BlockDie(x, y)
                entities.add(bd)
                platforms.append(bd)
            if col == "=":
                gr = Ground(x, y)
                entities.add(gr)
                platforms.append(gr)
            if col == "|":
                end = Endlvl(x, y)
                entities.add(end)
                platforms.append(end)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту
    """Создаём менюшку"""
    items = [(350, 300, u'Play', (11, 0, 77), (250, 250, 30), 0),
             (350, 340, u'Exit', (11, 0, 77), (250, 250, 30), 1)]
    game = Menu(items)
    game.menu()
    """Создаем монстров"""
    mn = Monster(700, 670, 2, 3, 150, 0)
    entities.add(mn)
    platforms.append(mn)
    monsters.add(mn)

    mn1 = Monster(300, 440, 1, 1, 50, 0)
    entities.add(mn1)
    platforms.append(mn1)
    monsters.add(mn1)

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while 1:  # Основной цикл программы
        timer.tick(60)
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                raise SystemExit("QUIT")
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_LSHIFT:
                running = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_LSHIFT:
                running = False

        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

        camera.update(hero)  # центризируем камеру относительно персонажа
        hero.update(left, right, up, running, platforms)  # передвижение
        monsters.update(platforms)
        # entities.draw(screen) # отображение
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()  # обновление и вывод всех изменений на экран


if __name__ == "__main__":
    main()
