#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import pygame
import sys
from sprites import *
from config import *
from utils import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font('assets/joystix monospace.otf', 32)
        self.character_spritesheet = Spritesheet('assets/img/Hero 01.png')
        self.terrain_spritesheet = Spritesheet('assets/img/Solaria Demo Update 01.png')
        self.enemy_spritesheet = Spritesheet('assets/img/Slime 01.png')
        self.intro_background = pygame.image.load('assets/img/introbackground.png')
        self.gameover_background = pygame.image.load('assets/img/gameover.png')
        self.attack_spritesheet = Spritesheet('assets/img/attack1.png')

    def createTilemap(self):
        layouts = {
            'ground': import_csv_layout('levels/level00_Ground.csv'),
            'bushes': import_csv_layout('levels/level00_Bushes.csv'),
            'player': import_csv_layout('levels/level00_Player.csv'),
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index
                        y = row_index
                        if style == 'bushes':
                            Decoration(self, x, y, col)
                        if style == 'ground':
                            Ground(self, x, y, col)
                        if style == 'player':
                            self.player = Player(self, x, y)

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.createTilemap()

    def events(self):
        # game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Attack(self, self.player.rect.x, self.player.rect.y)

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        # game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
        
    def game_over(self):

        text = self.font.render('Game Over', False, BLACK)
        text_rect = text.get_rect( center = (WIN_WIDTH / 2, WIN_HEIGHT / 2))

        restart_button = Button(10, WIN_HEIGHT - 60, 160, 50, WHITE, BLACK, 'Restart', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()
            self.screen.blit(self.gameover_background, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro = True
        
        title = self.font.render('RPG Game', True, BLACK)
        title_rect = title.get_rect(x = 10, y = 10)
        title_rect.x = int(WIN_WIDTH / 2 - title_rect.width / 2)

        play_button = Button(270, 215, 100, 50, RED, None, 'PLAY', 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()


def main():
    g = Game()
    g.intro_screen()
    g.new()
    while g.running:
        g.main()
        g.game_over()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
