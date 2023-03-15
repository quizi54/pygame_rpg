#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import pygame
import sys
from entitys import *
from sprites import *
from config import *
from utils import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(ASSETS['FONT'], 32)
        self.character_spritesheet = Spritesheet(ASSETS['HERO'])
        self.terrain_spritesheet = Spritesheet(ASSETS['TERRAIN'])
        self.enemy_spritesheet = Spritesheet(ASSETS['ENEMY'])
        self.intro_background = pygame.image.load(ASSETS['INTRO_BG'])
        self.gameover_background = pygame.image.load(ASSETS['GAMEOVER_BG'])
        self.attack_spritesheet = Spritesheet(ASSETS['ATTACK_PARTICLES'])

    def createTilemap(self):
        layouts = {
            'ground': import_csv_layout('assets/levels/level00_Ground.csv'),
            'bushes': import_csv_layout('assets/levels/level00_Bushes.csv'),
            'boundary': import_csv_layout('assets/levels/level00_Boundary.csv'),
            'enemies': import_csv_layout('assets/levels/level00_Enemies.csv'),
            'player': import_csv_layout('assets/levels/level00_Player.csv'),
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
                        if style == 'boundary':
                            Boundary(self, x, y)
                        if style == 'enemies':
                            Enemy(self, x, y)
                        if style == 'player':
                            self.player = Player(self, x, y)

    def new(self):
        self.playing = True

        self.visible_sprites = CameraGroup()
        self.boundary = pygame.sprite.LayeredUpdates()
        self.blocks   = pygame.sprite.LayeredUpdates()
        self.enemies  = pygame.sprite.LayeredUpdates()
        self.attacks  = pygame.sprite.LayeredUpdates()
        self.attackable_sprites = pygame.sprite.Group()
        self.createTilemap()

    def events(self):
        # game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False
                if event.key == pygame.K_SPACE:
                    Attack(self, self.player.rect.x, self.player.rect.y)

    def update(self):
        self.visible_sprites.update()
        self.player_attack_logic()

    def player_attack_logic(self):
        if self.attacks:
            for attack_sprite in self.attacks:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        target_sprite.hp -= self.player.damage
                        if target_sprite.hp <= 0:
                            self.player.experience += target_sprite.exp_cost
                            self.player.money += target_sprite.money
                            target_sprite.kill()
                            print(f'exp: {self.player.experience}  :: money: {self.player.money}')

    def draw(self):
        self.screen.fill(BLACK)
        self.visible_sprites.custom_draw(self.player)
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

        for sprite in self.visible_sprites:
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
