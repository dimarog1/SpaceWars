import random

import columns as columns
import pygame.rect

from ProgramFiles.base_classes import *
from ProgramFiles.player_sprites import ShotSpeedGain, ShotRangeGain, ShieldGain
from music.sounds import shoot_sound, boss_second_attack_sound


# --- Враги ---

class Enemy(Ship, pygame.sprite.Sprite):
    def __init__(self, screen, player, position=(0, -500)):
        Ship.__init__(self, screen, position)
        pygame.sprite.Sprite.__init__(self, enemy_group)
        self.speed_of_ship = 2
        self.border = 20
        self.hp_bar = HpBar(self, self.screen)
        self.__show_hp_bar = False
        self.shooting = False
        self.projectile = EnemyProjectileLevelOne
        self.speed_of_shooting = 50 - 5 * (COMPLEXITY - 1)
        self.chance = 20
        self.gains = (ShotSpeedGain, ShotRangeGain, ShieldGain)
        self.player = player

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
        do_spawn_gain = random.choices((True, False), weights=[self.chance, 100 - self.chance])[0]
        flag = True
        if do_spawn_gain:
            while flag:
                if len(shield_group) >= 1 and self.player.speed_of_shooting == 10 and self.player.level_of_projectiles == 4:
                    return
                gain = random.choice(self.gains)(self)
                print(flag)
                if len(shield_group) >= 1 and isinstance(gain, ShieldGain):
                    gain.kill()
                    continue
                if self.player.speed_of_shooting == 10 and isinstance(gain, ShotSpeedGain):
                    gain.kill()
                    continue
                if self.player.level_of_projectiles == 4 and isinstance(gain, ShotRangeGain):
                    gain.kill()
                    continue
                flag = False

    def shoot(self):
        enemy_shot = self.projectile(self)
        shoot_sound.play()

    def update(self):
        if self.border <= self.rect.x + self.speed_of_ship <= WIDTH - self.width - self.border:
            self.rect.x += self.speed_of_ship


# Враг первого уровня
class EnemyLevelOne(Enemy):
    def __init__(self, screen, player):
        Enemy.__init__(self, screen, player)
        self.image = pygame.transform.scale(load_image('enemy_level_one.png'), (70, 70))
        self.projectile = EnemyProjectileLevelOne
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hp = 50
        self.chance = 30
        self.hp_bar = HpBar(self, self.screen)


# Враг второго уровня
class EnemyLevelTwo(Enemy):
    def __init__(self, screen, player):
        Enemy.__init__(self, screen, player)
        self.image = pygame.transform.scale(load_image('enemy_level_two.png'), (90, 90))
        self.projectile = EnemyProjectileLevelTwo
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hp = 100
        self.chance = 40
        self.hp_bar = HpBar(self, self.screen)


# Враг третьего уровня
class EnemyLevelThree(Enemy):
    def __init__(self, screen, player):
        Enemy.__init__(self, screen, player)
        self.image = pygame.transform.scale(load_image('enemy_level_three.png'), (110, 110))
        self.projectile = EnemyProjectileLevelThree
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hp = 200
        self.chance = 50
        self.hp_bar = HpBar(self, self.screen)


# Враг четвёртого уровня
class EnemyLevelFour(Enemy):
    def __init__(self, screen, player):
        Enemy.__init__(self, screen, player)
        self.image = pygame.transform.scale(load_image('enemy_level_four.png'), (130, 130))
        self.projectile = EnemyProjectileLevelFour
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hp = 300
        self.chance = 60
        self.hp_bar = HpBar(self, self.screen)


# Босс
class Boss(Enemy):
    def __init__(self, screen, player):
        Enemy.__init__(self, screen, player)
        self.image = pygame.transform.scale(load_image('boss.png'), (130, 170))
        self.projectile_image = pygame.transform.scale(load_image('shot_level_four.png'), (110, 70))
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.max_hp = 4000
        self.hp = self.max_hp
        self.chance = 0
        self.speed_of_ship = 4
        self.hp_bar = HpBar(self, self.screen)
        self.attack_intervals = 220
        self.plug = 0
        self.attacks = [self.first_attack, self.second_attack]
        self.attack_type = -1
        self.projectile = EnemyProjectileLevelFour
        self.prev_attack = None

        # Пераметры для первой атаки
        self.attack_points = []
        self.point_to_move = 0

        # Пераметры для второй атаки
        self.attack_duration = 150
        self.shoots_interval = 15
        self.projectile_second_attack = BossProjectileSecondAttack

        # Пераметры для третьей атаки
        self.doing_third_attack = False
        self.waves = (
            [1, 3, 1],
            [2, 3, 2],
            [1, 4, 1],
            [2, 4, 2],
            [3, 4, 3],
        )

    def choose_attack(self):
        self.attack_points = [(random.randint(50, 650), random.randint(10, 200)), 0, 0]
        for ind in range(1, 3):
            flag = True
            while flag:
                x1, y1 = random.randint(50, 650), random.randint(10, 200)
                x2, y2 = self.attack_points[ind - 1]
                distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                if distance >= 300:
                    self.attack_points.insert(ind, (x1, y1))
                    flag = False
        flag = True
        self.attack_type = random.randint(1, 2)
        while flag:
            if self.attack_type == self.prev_attack == 2:
                self.attack_type = random.randint(1, 2)
            else:
                flag = False
        self.prev_attack = self.attack_type
        self.plug = 1

    def attack(self, count):
        if self.attack_type != -1:
            self.attacks[self.attack_type - 1](count)

    def first_attack(self, count=0):
        if self.point_to_move >= 3:
            self.attack_type = -1
            self.point_to_move = 0
            return
        point = self.attack_points[self.point_to_move]
        moves = ((0, self.speed_of_ship), (self.speed_of_ship, 0), (0, -self.speed_of_ship),
                 (-self.speed_of_ship, 0), (self.speed_of_ship, self.speed_of_ship),
                 (-self.speed_of_ship, -self.speed_of_ship), (-self.speed_of_ship, self.speed_of_ship),
                 (self.speed_of_ship, -self.speed_of_ship))
        results = []
        for move in moves:
            distance = ((point[0] - (self.rect.x + move[0])) ** 2
                        + (point[1] - (self.rect.y + move[1])) ** 2) ** 0.5
            results.append((move, distance))
        move, distance = min(results, key=lambda elem: elem[1])
        if distance > self.speed_of_ship:
            self.rect.x += move[0]
            self.rect.y += move[1]
        else:
            self.shoot()
            self.point_to_move += 1

    def second_attack(self, count):
        if self.attack_duration <= 0:
            self.attack_type = -1
            self.attack_duration = 150
            return
        if count % self.shoots_interval == 0:
            angles = (120, 150, 180, 210, 240)
            boss_second_attack_sound.play()
            for angle in angles:
                projectile = self.projectile_second_attack(self, angle)
        self.attack_duration -= 1

    def third_attack(self):
        return random.choice(self.waves)


# --- Выстрел ---
class EnemyProjectile(Projectile, pygame.sprite.Sprite):
    def __init__(self, parent_ship):
        Projectile.__init__(self, parent_ship)
        pygame.sprite.Sprite.__init__(self, enemy_shots_group)
        self.image = pygame.transform.scale(load_image('shot.png'), (17, 27))
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect().move(
            self.parent_ship.rect.x + self.parent_ship.width // 2 - self.width // 2,
            self.parent_ship.rect.y + self.parent_ship.height
        )
        self.speed_of_shot = 7

    def change_pos(self):
        if self.rect.y + self.speed_of_shot <= HEIGHT + self.height:
            self.rect.y += self.speed_of_shot
        else:
            self.kill()

    def update(self):
        # Столкновения с кораблём
        for shield in shield_group:
            if pygame.sprite.collide_mask(self, shield):
                shield.hp -= 1
                self.kill()
                return

        for player in player_group:
            if pygame.sprite.collide_mask(self, player):
                player.reduce_hp()
                self.kill()
                return

        # Перемщение снаряда
        self.change_pos()


class EnemyProjectileLevelOne(EnemyProjectile):
    def __init__(self, parent_ship):
        EnemyProjectile.__init__(self, parent_ship)
        self.image = pygame.transform.scale(load_image('shot.png'), (17, 27))
        self.image = pygame.transform.rotate(self.image, 180)
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect().move(
            self.parent_ship.rect.x + self.parent_ship.width // 2 - self.width // 2,
            self.parent_ship.rect.y + self.parent_ship.height
        )


class EnemyProjectileLevelTwo(EnemyProjectile):
    def __init__(self, parent_ship):
        EnemyProjectile.__init__(self, parent_ship)
        self.image = pygame.transform.scale(load_image('shot_level_two.png'), (40, 30))
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect().move(
            self.parent_ship.rect.x + self.parent_ship.width // 2 - self.width // 2,
            self.parent_ship.rect.y + self.parent_ship.height
        )


class EnemyProjectileLevelThree(EnemyProjectile):
    def __init__(self, parent_ship):
        EnemyProjectile.__init__(self, parent_ship)
        self.image = pygame.transform.scale(load_image('shot_level_three.png'), (70, 40))
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect().move(
            self.parent_ship.rect.x + self.parent_ship.width // 2 - self.width // 2,
            self.parent_ship.rect.y + self.parent_ship.height
        )


class EnemyProjectileLevelFour(EnemyProjectile):
    def __init__(self, parent_ship):
        EnemyProjectile.__init__(self, parent_ship)
        self.image = pygame.transform.scale(load_image('shot_level_four.png'), (110, 70))
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect().move(
            self.parent_ship.rect.x + self.parent_ship.width // 2 - self.width // 2,
            self.parent_ship.rect.y + self.parent_ship.height
        )


class BossProjectileSecondAttack(EnemyProjectileLevelOne):
    def __init__(self, parent_ship, angle):
        EnemyProjectileLevelOne.__init__(self, parent_ship)
        self.angle = angle
        self.image = pygame.transform.rotate(self.image, 180)
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed_of_shot_y = 10
        if self.angle == 120:
            self.speed_of_shot_x = -10
            self.speed_of_shot_y = -0.4 * self.speed_of_shot_x
        elif self.angle == 150:
            self.speed_of_shot_x = -5
            self.speed_of_shot_y = -1.5 * self.speed_of_shot_x
        elif self.angle == 180:
            self.speed_of_shot_x = 0
            self.speed_of_shot_y = 10
        elif self.angle == 210:
            self.speed_of_shot_x = 5
            self.speed_of_shot_y = 1.5 * self.speed_of_shot_x
        elif self.angle == 240:
            self.speed_of_shot_x = 10
            self.speed_of_shot_y = 0.4 * self.speed_of_shot_x

    def change_pos(self):
        if self.rect.y + self.speed_of_shot <= HEIGHT + self.height \
                and 0 <= self.rect.x + self.speed_of_shot <= WIDTH + self.width:
            self.rect.x += self.speed_of_shot_x
            self.rect.y += self.speed_of_shot_y
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


# враг в меню
class SecretEnemy(Enemy):
    def __init__(self, screen, player):
        Enemy.__init__(self, screen, player)
        self.image = pygame.transform.scale(load_image('secret_enemy.png'), (170, 200))
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def change_pos(self, dx, dy):
        if 50 <= self.rect.x + dx * self.speed_of_ship <= WIDTH - self.width - 50:
            self.rect = self.rect.move(
                self.speed_of_ship * dx,
                self.speed_of_ship * dy
            )
        else:
            self.speed_of_ship *= -1
