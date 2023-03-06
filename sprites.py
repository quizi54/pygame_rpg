import pygame
from config import *
import math, random


class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height, bg):
        """
        Return single sprite from spritesheet file.
        x - x-coordinates
        y - y-coordinates
        width - width of tile 
        height - height of tile 
        """
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(bg)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        #self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height, WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    def collide_blocks(self, direction):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if direction == 'x':
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
        if direction == 'y':
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False

    def animate(self):
        down_animations = [
                self.game.character_spritesheet.get_sprite(0, 64, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(16, 64, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(32, 64, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(48, 64, self.width, self.height, BLACK) ]
        up_animations = [
                self.game.character_spritesheet.get_sprite(0, 48, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(16, 48, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(32, 48, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(48, 48, self.width, self.height, BLACK) ]
        left_animations = [
                self.game.character_spritesheet.get_sprite(0, 16, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(16, 16, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(32, 16, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(48, 16, self.width, self.height, BLACK) ]
        right_animations = [
                self.game.character_spritesheet.get_sprite(0, 32, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(16, 32, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(32, 32, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(48, 32, self.width, self.height, BLACK) ]
        current_animation = []

        if self.facing == 'down':
            current_animation = down_animations[:]
        if self.facing == 'up':
            current_animation = up_animations[:]
        if self.facing == 'left':
            current_animation = left_animations[:]
        if self.facing == 'right':
            current_animation = right_animations[:]

        if (self.facing in ('down', 'up') and self.y_change == 0) or (self.facing in ('left', 'right') and self.x_change == 0):
            self.image = current_animation[0]
        else:
            self.image = current_animation[math.floor(self.animation_loop)]
            self.animation_loop += 0.1
            if self.animation_loop >= 3:
                self.animation_loop = 0

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0 
        self.max_travel = random.randint(7, 30)

        self.image = self.game.enemy_spritesheet.get_sprite(0, 0, self.width, self.height, WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1 
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'
        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1 
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

    def animate(self):
        left_animations = [
                self.game.enemy_spritesheet.get_sprite(0, 16, self.width, self.height, BLACK),
                self.game.enemy_spritesheet.get_sprite(16, 16, self.width, self.height, BLACK),
                self.game.enemy_spritesheet.get_sprite(32, 16, self.width, self.height, BLACK),
                self.game.enemy_spritesheet.get_sprite(48, 16, self.width, self.height, BLACK) ]
        right_animations = [
                self.game.enemy_spritesheet.get_sprite(0, 32, self.width, self.height, BLACK),
                self.game.enemy_spritesheet.get_sprite(16, 32, self.width, self.height, BLACK),
                self.game.enemy_spritesheet.get_sprite(32, 32, self.width, self.height, BLACK),
                self.game.enemy_spritesheet.get_sprite(48, 32, self.width, self.height, BLACK) ]
        current_animation = []

        if self.facing == 'left':
            current_animation = left_animations[:]
        if self.facing == 'right':
            current_animation = right_animations[:]

        if  self.facing in ('left', 'right') and self.x_change == 0:
            self.image = current_animation[0]
        else:
            self.image = current_animation[math.floor(self.animation_loop)]
            self.animation_loop += 0.1
            if self.animation_loop >= 3:
                self.animation_loop = 0

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(400, 128, self.width, self.height, BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(80, 0, self.width, self.height, BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('PixeloidMono.ttf', fontsize)
        self.content = content
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fg = fg 
        self.bg = bg
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.text = self.font.render(self.content, False, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width / 2, self.height / 2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
