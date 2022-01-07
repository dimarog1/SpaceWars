import random

import pygame.rect

from ProgramFiles.base_classes import *
from ProgramFiles.player_sprites import ShotSpeedGain, ShotRangeGain, ShieldGain


# --- Враги ---

class Enemy(Ship, pygame.sprite.Sprite):
    def __init__(self, screen, position=(0, -500)):
        Ship.__init__(self, screen, position)
        pygame.sprite.Sprite.__init__(self, enemy_group)
        self.speed_of_ship = 2
        self.border = 20
        self.hp_bar = HpBar(self, self.screen)
        self.__show_hp_bar = False
        self.shooting = False
        self.speed_of_shooting = 60
        self.gains = (ShotSpeedGain, ShotRangeGain, ShieldGain)

    def set_start_pos(self, x, y):
        self.rect = self.image.get_rect().move(x, y)

    def check_is_ship_on_screen(self):
        if self.border <= self.rect.x + self.speed_of_ship <= WIDTH - self.width - self.border:
            return True
        return False

    def activate_hp_bar(self):
        self.__show_hp_bar = True

    def draw_hp_bar(self):
        if self.__show_hp_bar:
            self.hp_bar.draw()

    def check_alive(self):
        # Проверяем количство hp
        if self.hp <= 0:
            self.spawn_gain()
            self.kill()
            boom = BoomSprite(self)
            boom_sound.play()

    def spawn_gain(self):
        do_spawn_gain = random.choices((True, False), weights=[40, 60])[0]
        flag = True
        if do_spawn_gain:
            while flag:
                gain = random.choice(self.gains)(self)
                if len(shield_group) >= 1 and isinstance(gain, ShieldGain):
                    continue
                flag = False

    def update(self):
        if self.border <= self.rect.x + self.speed_of_ship <= WIDTH - self.width - self.border:
            self.rect.x += self.speed_of_ship


# Враг первого уровня
class EnemyLevelOne(Enemy):
    def __init__(self, screen):
        Enemy.__init__(self, screen)
        self.image = pygame.transform.scale(load_image('enemy_level_one.png'), (70, 70))
        self.projectile_image = pygame.transform.scale(load_image('shot.png'), (17, 27))
        self.projectile_image = pygame.transform.rotate(self.projectile_image, 180)
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hp = 50
        self.hp_bar = HpBar(self, self.screen)

    # def change_pos(self, dx, dy):
    #     if 50 <= self.rect.x + dx * self.speed_of_ship <= WIDTH - self.width - 50:
    #         self.rect = self.rect.move(
    #             self.speed_of_ship * dx,
    #             self.speed_of_ship * dy
    #         )
    #     else:
    #         self.speed_of_ship *= -1


# Враг второго уровня
class EnemyLevelTwo(Enemy):
    def __init__(self, screen):
        Enemy.__init__(self, screen)
        self.image = pygame.transform.scale(load_image('enemy_level_two.png'), (90, 90))
        self.projectile_image = pygame.transform.scale(load_image('shot_level_two.png'), (40, 30))
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hp = 100
        self.hp_bar = HpBar(self, self.screen)


# Враг третьего уровня
class EnemyLevelThree(Enemy):
    def __init__(self, screen):
        Enemy.__init__(self, screen)
        self.image = pygame.transform.scale(load_image('enemy_level_three.png'), (110, 110))
        self.projectile_image = pygame.transform.scale(load_image('shot_level_three.png'), (70, 40))
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hp = 200
        self.hp_bar = HpBar(self, self.screen)


# Враг четвёртого уровня
class EnemyLevelFour(Enemy):
    def __init__(self, screen):
        Enemy.__init__(self, screen)
        self.image = pygame.transform.scale(load_image('enemy_level_four.png'), (130, 130))
        self.projectile_image = pygame.transform.scale(load_image('shot_level_four.png'), (110, 70))
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hp = 300
        self.hp_bar = HpBar(self, self.screen)


# --- Выстрел ---
class EnemyProjectile(Projectile, pygame.sprite.Sprite):
    def __init__(self, parent_ship):
        Projectile.__init__(self, parent_ship)
        pygame.sprite.Sprite.__init__(self, enemy_shots_group)
        self.image = parent_ship.projectile_image
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect().move(
            self.parent_ship.rect.x + self.parent_ship.width // 2 - self.width // 2,
            self.parent_ship.rect.y + self.parent_ship.height
        )
        self.speed_of_shot = 6

    def update(self):
        # Столкновения с кораблём
        for shield in shield_group:
            if pygame.sprite.collide_mask(self, shield):
                shield.hp -= 1
                self.kill()
                return

        for player in player_group:
            if pygame.sprite.collide_mask(self, player):
                player.hp -= 1
                self.kill()
                return

        # Перемщение снаряда
        if self.rect.y + self.speed_of_shot <= HEIGHT + self.height:
            self.rect.y += self.speed_of_shot
        else:
            self.kill()


class HpBar:
    def __init__(self, parent, screen):
        self.parent = parent
        self.screen = screen
        self.max_hp = self.parent.hp
        self.color = pygame.Color('green')
        self.x1 = self.parent.rect.x
        self.y1 = self.parent.rect.y + self.parent.height + 5
        self.w = self.parent.width
        self.h = 10
        self.parts = self.parent.width / self.max_hp

    def draw(self):
        hp_percent = self.parent.hp / self.max_hp
        if hp_percent <= 0.2:
            self.color = pygame.Color('red')
        elif hp_percent <= 0.6:
            self.color = pygame.Color('orange')
        self.x1 = self.parent.rect.x
        self.y1 = self.parent.rect.y + self.parent.height + 5
        pygame.draw.rect(self.screen, self.color, (self.x1, self.y1,
                                                   self.w * (self.parent.hp / self.max_hp), self.h))
