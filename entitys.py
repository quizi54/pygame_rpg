import pygame
from sprites import *
from config import *
import math, random


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.visible_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        # direction & coordinates
        self.x = x * TILESIZE
        self.y = y * TILESIZE - 16
        self.width  = TILESIZE
        self.height = TILESIZE + 16
        self.x_change = 0
        self.y_change = 0
        self.direction = pygame.math.Vector2()
        self.direction.y = 1
        self.last_direction = 2

        # image & animation
        self.animation_loop = 1
        self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height, BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.idle_animations  = [
                self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height, BLACK)]
        self.down_animations  = [
                self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(32, 0, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(64, 0, self.width, self.height, BLACK)]
        self.up_animations    = [
                self.game.character_spritesheet.get_sprite(0, 144, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(32, 144, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(64, 144, self.width, self.height, BLACK) ]
        self.left_animations  = [
                self.game.character_spritesheet.get_sprite(0, 48, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(32, 48, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(64, 48, self.width, self.height, BLACK) ]
        self.right_animations = [
                self.game.character_spritesheet.get_sprite(0, 96, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(32, 96, self.width, self.height, BLACK),
                self.game.character_spritesheet.get_sprite(64, 96, self.width, self.height, BLACK) ]

        # parameters
        self.level = 1
        self.experience = 0
        self.money = 0
        # base atributes
        self.strength = 10
        self.dexterity = 10
        self.intelligence = 10
        self.health = 10

        self.base_hp = int(self.health + self.strength * 0.3)
        self.hp = self.base_hp
        self.damage = int(self.strength * 0.8)

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
            self.direction.x = -1
            self.x_change -= PLAYER_SPEED
            self.last_direction = 3
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.x_change += PLAYER_SPEED
            self.last_direction = 1
        else:
            self.direction.x = 0
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.y_change -= PLAYER_SPEED
            self.last_direction = 0
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.y_change += PLAYER_SPEED
            self.last_direction = 2
        else:
            self.direction.y = 0

    def collide_blocks(self, direction):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if direction == 'x':
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.visible_sprites:
                        sprite.rect.x += PLAYER_SPEED
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.visible_sprites:
                        sprite.rect.x -= PLAYER_SPEED
        if direction == 'y':
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.visible_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.visible_sprites:
                        sprite.rect.y -= PLAYER_SPEED

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False

    def animate(self):
        current_animation = []
        if self.direction.y == 1:
            current_animation = self.down_animations
        if self.direction.y == -1:
            current_animation = self.up_animations
        if self.direction.x == -1:
            current_animation = self.left_animations
        if self.direction.x == 1:
            current_animation = self.right_animations
        if self.direction.length() == 0:
            current_animation = self.idle_animations
        if self.y_change == 0 and self.x_change == 0:
            if self.last_direction == 0:
                self.image = self.up_animations[0]
            elif self.last_direction == 1:
                self.image = self.right_animations[0]
            elif self.last_direction == 2:
                self.image = self.down_animations[0]
            elif self.last_direction == 3:
                self.image = self.left_animations[0]
        else:
            self.image = current_animation[math.floor(self.animation_loop)]
            self.animation_loop += 0.15
            if self.animation_loop >= 3:
                self.animation_loop = 0


class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.visible_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        if self.game.player.last_direction == 1:
            self.direction = 'right'
        elif self.game.player.last_direction == 3:
            self.direction = 'left'
        if self.game.player.last_direction == 2:
            self.direction = 'down'
        elif self.game.player.last_direction == 0:
            self.direction = 'up'

        if self.direction == 'down':
            self.y = y + TILESIZE * 1.2
            self.x = x
        if self.direction == 'up':
            self.y = y - TILESIZE // 2
            self.x = x
        if self.direction == 'left':
            self.x = x - TILESIZE
            self.y = y + TILESIZE // 2
        if self.direction == 'right':
            self.x = x + TILESIZE
            self.y = y + TILESIZE // 2

        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0
        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height, BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.right_animations = [
                self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height, BLACK) ]
        self.up_animations = [
                self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height, BLACK) ]
        self.left_animations = [
                self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height, BLACK) ]
        self.down_animations = [
                self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height, BLACK),
                self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height, BLACK) ]

    def update(self):
        self.animate()
        # self.collide()

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
        if self.animation_loop >= 4:
            self.kill()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.game.enemies[0].hp -= self.game.player.damage
            if self.game.enemies[0].hp <= 0:
                self.game.player.experience += self.game.enemies[0].exp_cost
                self.game.player.money += self.game.enemies[0].money
                self.game.enemies[0].kill()
                print(f'exp: {self.game.player.experience}  :: money: {self.game.player.money}')

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.visible_sprites, self.game.enemies, self.game.attackable_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.x_change = 0
        self.y_change = 0

        self.hp = 10
        self.exp_cost = 10
        self.money = 2

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0 
        self.max_travel = random.randint(7, 30)

        self.image = self.game.enemy_spritesheet.get_sprite(0, 0, self.width, self.height, WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.left_animations = [
                self.game.enemy_spritesheet.get_sprite(288, 160, self.width, self.height, BLACK),
                self.game.enemy_spritesheet.get_sprite(320, 160, self.width, self.height, BLACK),
                self.game.enemy_spritesheet.get_sprite(352, 160, self.width, self.height, BLACK),
                self.game.enemy_spritesheet.get_sprite(320, 160, self.width, self.height, BLACK) ]
        self.right_animations = [
                self.game.enemy_spritesheet.get_sprite(288, 192, self.width, self.height, BLACK),
                self.game.enemy_spritesheet.get_sprite(320, 192, self.width, self.height, BLACK),
                self.game.enemy_spritesheet.get_sprite(352, 192, self.width, self.height, BLACK),
                self.game.enemy_spritesheet.get_sprite(320, 192, self.width, self.height, BLACK) ]

    def update(self):
        self.movement()
        self.animate()
        # self.collide_blocks()
        self.rect.x += self.x_change
        # self.rect.y += self.y_change

        self.x_change = 0
        # self.y_change = 0

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
            if self.animation_loop >= 4:
                self.animation_loop = 0
