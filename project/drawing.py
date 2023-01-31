import pygame
import pyglet
from settings import *
from ray_casting import ray_casting
from map import mini_map
from collections import deque
from random import  randrange
import sys

class Drawing:
    def __init__(self, sc, sc_map, player, clock):
        self.sc = sc
        self.sc_map = sc_map
        self.player = player
        self.clock = clock
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.font_win = pygame.font.Font('font/Alien-Ravager-Italic.ttf', 100)
        self.textures = {1: pygame.image.load('img/wall0.png').convert(),
                         2: pygame.image.load('img/wall02.png').convert(),
                         3: pygame.image.load('img/wall01.png').convert(),
                         4: pygame.image.load('img/wall00.png').convert(),
                         5: pygame.image.load('img/FLOOR.png').convert(),
                         'S': pygame.image.load('img/sky1.png').convert(),
                         'S2': pygame.image.load('img/sky2.png').convert(),
                         }
        self.menu_trigger = True
        self.menu_picture = pygame.image.load('img/bg.jpg').convert()
        self.weapon_base_sprite = pygame.image.load('sprites/weapons/shotgun/base/0.png').convert_alpha()
        self.weapon_shot_animation = deque([pygame.image.load(f'sprites/weapons/shotgun/shot/{i}.png').convert_alpha()
                                            for i in range(6)])
        self.weapon_rect = self.weapon_base_sprite.get_rect()
        self.weapon_pos = (HALF_WIDTH - self.weapon_rect.width // 2, HEIGHT - self.weapon_rect.height)
        self.shot_length = len(self.weapon_shot_animation)
        self.shot_length_count = 0
        self.shot_animation_speed = 2
        self.shot_animation_count = 0
        self.shot_animation_trigger = True
        self.shot_sound = pygame.mixer.Sound('sound/shotgun.wav')
        # sfx parameters
        self.sfx = deque([pygame.image.load(f'sprites/weapons/sfx/{i}.png').convert_alpha() for i in range(9)])
        self.sfx_length_count = 0
        self.sfx_length = len(self.sfx)

    def background(self, angle):
        sky_offset = -10 * math.degrees(angle) % WIDTH
        if now_lew == 1:
            self.sc.blit(self.textures['S'], (sky_offset, 0))
            self.sc.blit(self.textures['S'], (sky_offset - WIDTH, 0))
            self.sc.blit(self.textures['S'], (sky_offset + WIDTH, 0))
            a = pygame.draw.rect(self.sc, DARKGRAY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))
            self.sc.blit(self.textures['S'], (sky_offset + WIDTH, 0))
        else:
            self.sc.blit(self.textures['S2'], (sky_offset, 0))
            self.sc.blit(self.textures['S2'], (sky_offset - WIDTH, 0))
            self.sc.blit(self.textures['S2'], (sky_offset + WIDTH, 0))
            a = pygame.draw.rect(self.sc, DARKGRAY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))
            self.sc.blit(self.textures['S2'], (sky_offset + WIDTH, 0))

    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.sc.blit(object, object_pos)

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, DARKORANGE)
        self.sc.blit(render, FPS_POS)

    def mini_map(self, player):
        self.sc_map.fill(BLACK)
        map_x, map_y = player.x // MAP_SCALE, player.y // MAP_SCALE
        pygame.draw.line(self.sc_map, YELLOW, (map_x, map_y), (map_x + 12 * math.cos(player.angle),
                                                 map_y + 12 * math.sin(player.angle)), 2)
        pygame.draw.circle(self.sc_map, RED, (int(map_x), int(map_y)), 5)
        for x, y in mini_map:
            pygame.draw.rect(self.sc_map, RED, (x, y, MAP_TILE, MAP_TILE))
        self.sc.blit(self.sc_map, MAP_POS)

    def player_weapon(self, shots):
        if self.player.shot:
            if not self.shot_length_count:
                self.shot_sound.play()
                global SHC
                SHC += 1
            self.shot_projection = min(shots)[1] // 2
            self.bullet_sfx()
            shot_sprite = self.weapon_shot_animation[0]
            self.sc.blit(shot_sprite, self.weapon_pos)
            self.shot_animation_count += 1
            if self.shot_animation_count == self.shot_animation_speed:
                self.weapon_shot_animation.rotate(-1)
                self.shot_animation_count = 0
                self.shot_length_count += 1
                self.shot_animation_trigger = False
            if self.shot_length_count == self.shot_length:
                self.player.shot = False
                self.shot_length_count = 0
                self.sfx_length_count = 0
                self.shot_animation_trigger = True
        else:
            self.sc.blit(self.weapon_base_sprite, self.weapon_pos)

    def bullet_sfx(self):
        if self.sfx_length_count < self.sfx_length:
            sfx = pygame.transform.scale(self.sfx[0], (self.shot_projection, self.shot_projection))
            sfx_rect = sfx.get_rect()
            self.sc.blit(sfx, (HALF_WIDTH - sfx_rect.w // 2, HALF_HEIGHT - sfx_rect.h // 2))
            self.sfx_length_count += 1
            self.sfx.rotate(-1)

    def win(self):
        render = self.font_win.render('YOU WIN!!!', 1, (randrange(40, 120), 0, 0))
        render2 = self.font_win.render(f'you score: {round((13 / SHC * 100), 2) }', 1, (randrange(40, 120), 0, 0))
        rect = pygame.Rect(0, 0, 1000, 500)
        rect.center = HALF_WIDTH, HALF_HEIGHT
        pygame.draw.rect(self.sc, BLACK, rect, border_radius=50)
        self.sc.blit(render, (rect.centerx - 430, rect.centery - 140))
        self.sc.blit(render2, (rect.centerx - 430, rect.centery - 40))
        if now_lew == 1:
            with open("info.txt") as file:
                data = file.readlines()
                data[0] = '2' + "\n"
            with open("info.txt", 'wt') as file:
                for i in data:
                    file.write(''.join(i))
        pygame.display.flip()
        self.clock.tick(5)


    def menu(self):
        x = 0

        while self.menu_trigger:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            button_font = pygame.font.Font('font/Alien-Ravager-Italic.ttf', 72)
            label_font = pygame.font.Font('font/Alien-Ravager-Italic.otf', 100)
            label_font2 = pygame.font.Font('font/Alien-Ravager-Italic.otf', 150)
            start = button_font.render('LEVELS', 1, pygame.Color('lightgray'))
            button_start = pygame.Rect(0, 0, 400, 150)
            button_start.center = HALF_WIDTH, HALF_HEIGHT
            exit = button_font.render('EXIT', 1, pygame.Color('lightgray'))
            button_exit = pygame.Rect(0, 0, 400, 150)
            button_exit.center = HALF_WIDTH, HALF_HEIGHT + 200

            self.sc.blit(self.menu_picture, (0, 0))
            x += 1


            pygame.draw.rect(self.sc, BLACK, button_start, border_radius=15, width=10)
            self.sc.blit(start, (button_start.centerx - 130, button_start.centery - 70))

            pygame.draw.rect(self.sc, BLACK, button_exit, border_radius=15, width=10)
            self.sc.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))

            color = randrange(40)
            label = label_font.render('Cyber War', 1,  pygame.Color('lightgray'))
            self.sc.blit(label, (10, HALF_HEIGHT - 400))
            label2 = label_font2.render('2@88', 1,  pygame.Color('lightgray'))
            self.sc.blit(label2, (300, HALF_HEIGHT - 355))

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if button_start.collidepoint(mouse_pos):
                pygame.draw.rect(self.sc, BLACK, button_start, border_radius=15)
                self.sc.blit(start, (button_start.centerx - 130, button_start.centery - 70))
                if mouse_click[0]:
                    self.menu_trigger = False
            elif button_exit.collidepoint(mouse_pos):
                pygame.draw.rect(self.sc, BLACK, button_exit, border_radius=15)
                self.sc.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))
                if mouse_click[0]:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            self.clock.tick(20)

        self.menu_trigger2 = True

        while self.menu_trigger2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            button_font = pygame.font.Font('font/Alien-Ravager-Italic.ttf', 72)
            label_font = pygame.font.Font('font/Alien-Ravager-Italic.otf', 100)
            label_font2 = pygame.font.Font('font/Alien-Ravager-Italic.otf', 150)
            if now_lew == 1:
                start = button_font.render('LEVEL 1', 1, pygame.Color('lightgray'))
                button_start = pygame.Rect(0, 0, 400, 150)
                button_start.center = HALF_WIDTH, HALF_HEIGHT
                exit = button_font.render('   x', 1, pygame.Color('lightgray'))
                button_exit = pygame.Rect(0, 0, 400, 150)
                button_exit.center = HALF_WIDTH, HALF_HEIGHT + 200
            else:
                start = button_font.render('    X', 1, pygame.Color('lightgray'))
                button_start = pygame.Rect(0, 0, 400, 150)
                button_start.center = HALF_WIDTH, HALF_HEIGHT
                exit = button_font.render('LEVEL 2', 1, pygame.Color('lightgray'))
                button_exit = pygame.Rect(0, 0, 400, 150)
                button_exit.center = HALF_WIDTH, HALF_HEIGHT + 200

            self.sc.blit(self.menu_picture, (0, 0))
            x += 1

            pygame.draw.rect(self.sc, BLACK, button_start, border_radius=15, width=10)
            self.sc.blit(start, (button_start.centerx - 130, button_start.centery - 70))

            pygame.draw.rect(self.sc, BLACK, button_exit, border_radius=15, width=10)
            self.sc.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))

            color = randrange(40)
            label = label_font.render('Cyber War', 1, pygame.Color('lightgray'))
            self.sc.blit(label, (10, HALF_HEIGHT - 400))
            label2 = label_font2.render('2@88', 1, pygame.Color('lightgray'))
            self.sc.blit(label2, (300, HALF_HEIGHT - 355))

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if button_start.collidepoint(mouse_pos):
                pygame.draw.rect(self.sc, BLACK, button_start, border_radius=15)
                self.sc.blit(start, (button_start.centerx - 130, button_start.centery - 70))
                if mouse_click[0]:
                    if now_lew == 1:
                        self.menu_trigger2 = False
                    else:
                        pass

            elif button_exit.collidepoint(mouse_pos):
                pygame.draw.rect(self.sc, BLACK, button_exit, border_radius=15)
                self.sc.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))
                if mouse_click[0]:
                    if now_lew == 2:
                        self.menu_trigger2 = False
                    else:
                        pass
            pygame.display.flip()
            self.clock.tick(20)
