import pygame
from config import *
import math, random


class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()

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

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.visible_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(400, 128, self.width, self.height, BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Boundary(Block):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.groups = self.game.blocks
        self.image = pygame.Surface((self.width, self.height), flags=pygame.SRCALPHA)

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y, tile_id):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.visible_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.tile_id = int(tile_id)

        tile_x, tile_y = self.get_tile_coords()

        self.image = self.game.terrain_spritesheet.get_sprite(tile_x, tile_y, self.width, self.height, BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def get_tile_coords(self):
        if self.tile_id > 27:
            y = (self.tile_id // 27) * TILESIZE
            x = (self.tile_id - 28 * (self.tile_id // 27)) * TILESIZE
        else:
            y = 0
            x = self.tile_id * TILESIZE
        return x, y

class Decoration(Ground):
    def __init__(self, game, x, y, tile_id):
        super().__init__(game, x, y, tile_id)
        self._layer = BLOCK_LAYER

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('assets/joystix monospace.otf', fontsize)
        self.content = content
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fg = fg 
        self.bg = bg
        
        if bg is not None:
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(self.bg)
        else:
            self.image = pygame.Surface((self.width, self.height), flags=pygame.SRCALPHA)
        
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

