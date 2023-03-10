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

        self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height, BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [
                self.game.character_spritesheet.get_sprite(0, 64, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(16, 64, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(32, 64, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(48, 64, self.width, self.height, BLACK) ]
        self.up_animations = [
                self.game.character_spritesheet.get_sprite(0, 48, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(16, 48, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(32, 48, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(48, 48, self.width, self.height, BLACK) ]
        self.left_animations = [
                self.game.character_spritesheet.get_sprite(0, 16, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(16, 16, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(32, 16, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(48, 16, self.width, self.height, BLACK) ]
        self.right_animations = [
                self.game.character_spritesheet.get_sprite(0, 32, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(16, 32, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(32, 32, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(48, 32, self.width, self.height, BLACK) ]

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
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
        if direction == 'y':
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False

    def animate(self):
        current_animation = []
        if self.facing == 'down':
            current_animation = self.down_animations
        if self.facing == 'up':
            current_animation = self.up_animations
        if self.facing == 'left':
            current_animation = self.left_animations
        if self.facing == 'right':
            current_animation = self.right_animations

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

        self.left_animations = [
                self.game.enemy_spritesheet.get_sprite(0, 16, self.width, self.height, BLACK),
                self.game.enemy_spritesheet.get_sprite(16, 16, self.width, self.height, BLACK),
                self.game.enemy_spritesheet.get_sprite(32, 16, self.width, self.height, BLACK),
                self.game.enemy_spritesheet.get_sprite(48, 16, self.width, self.height, BLACK) ]
        self.right_animations = [
                self.game.enemy_spritesheet.get_sprite(0, 32, self.width, self.height, BLACK),
                self.game.enemy_spritesheet.get_sprite(16, 32, self.width, self.height, BLACK),
                self.game.enemy_spritesheet.get_sprite(32, 32, self.width, self.height, BLACK),
                self.game.enemy_spritesheet.get_sprite(48, 32, self.width, self.height, BLACK) ]

    def update(self):
        self.movement()
        self.animate()
        # self.collide_blocks()
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

    def collide_blocks(self):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if hits:
            if self.x_change > 0:
                self.rect.x = hits[0].rect.left - self.rect.width
                self.facing = 'right'
            if self.x_change < 0:
                self.rect.x = hits[0].rect.right
                self.facing = 'left'

    def animate(self):
        current_animation = []

        if self.facing == 'left':
            current_animation = self.left_animations
        if self.facing == 'right':
            current_animation = self.right_animations

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
    def __init__(self, game, x, y, tile_id):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
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
        self.font = pygame.font.Font('PixeloidMono.ttf', fontsize)
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

class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = [self.game.all_sprites, self.game.attacks]
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.direction = self.game.player.facing
        if self.direction == 'down':
            self.y = y + TILESIZE
            self.x = x
        if self.direction == 'up':
            self.y = y - TILESIZE
            self.x = x
        if self.direction == 'left':
            self.x = x - TILESIZE
            self.y = y
        if self.direction == 'right':
            self.x = x + TILESIZE
            self.y = y

        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0
        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height, BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.right_animations = [
                self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(16, 32, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(48, 32, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height, BLACK) ]
        self.up_animations = [
                self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(16, 0, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(48, 0, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height, BLACK) ]
        self.left_animations = [
                self.game.attack_spritesheet.get_sprite(0, 48, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(16, 48, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(32, 48, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(48, 48, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(64, 48, self.width, self.height, BLACK) ]
        self.down_animations = [
                self.game.attack_spritesheet.get_sprite(0, 16, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(16, 16, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(32, 16, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(48, 16, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(64, 16, self.width, self.height, BLACK) ]

    def update(self):
        self.animate()
        self.collide()

    def animate(self):
        current_animation = []

        if self.direction == 'down':
            current_animation = self.down_animations
        if self.direction == 'up':
            current_animation = self.up_animations
        if self.direction == 'left':
            current_animation = self.left_animations
        if self.direction == 'right':
            current_animation = self.right_animations

        self.image = current_animation[math.floor(self.animation_loop)]
        self.animation_loop += 0.5
        if self.animation_loop >= 5:
            self.kill()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            pass