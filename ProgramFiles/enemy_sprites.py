import pygame.rect

from ProgramFiles.base_classes import *


# --- Враги ---

class Enemy(Ship, pygame.sprite.Sprite):
    def __init__(self, position=(0, -500)):
        Ship.__init__(self, position)
        pygame.sprite.Sprite.__init__(self, enemy_group)

    def set_start_pos(self, x, y):
        self.rect = self.image.get_rect().move(x, y)


# Враг первого уровня
class EnemyLevelOne(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.image = pygame.transform.scale(load_image('enemy_level_one.png'), (70, 70))
        self.projectile_image = pygame.transform.scale(load_image('shot.png'), (17, 27))
        self.projectile_image = pygame.transform.rotate(self.projectile_image, 180)
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed_of_ship = 3
        self.hp = 5

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
    def __init__(self):
        Enemy.__init__(self)
        self.image = pygame.transform.scale(load_image('enemy_level_two.png'), (90, 90))
        self.projectile_image = pygame.transform.scale(load_image('enemy_shot_level_two.png'), (40, 30))
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed_of_ship = 3
        self.hp = 10

    def change_pos(self, dx, dy):
        if 50 <= self.rect.x + dx * self.speed_of_ship <= WIDTH - self.width - 50:
            self.rect = self.rect.move(
                self.speed_of_ship * dx,
                self.speed_of_ship * dy
            )
        else:
            self.speed_of_ship *= -1


# Враг третьего уровня
class EnemyLevelThree(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.image = pygame.transform.scale(load_image('enemy_level_three.png'), (110, 110))
        self.projectile_image = pygame.transform.scale(load_image('enemy_shot_level_three.png'), (70, 40))
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed_of_ship = 3
        self.hp = 20

    def change_pos(self, dx, dy):
        if 50 <= self.rect.x + dx * self.speed_of_ship <= WIDTH - self.width - 50:
            self.rect = self.rect.move(
                self.speed_of_ship * dx,
                self.speed_of_ship * dy
            )
        else:
            self.speed_of_ship *= -1


# Враг четвёртого уровня
class EnemyLevelFour(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.image = pygame.transform.scale(load_image('enemy_level_four.png'), (130, 130))
        self.projectile_image = pygame.transform.scale(load_image('enemy_shot_level_four.png'), (110, 70))
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed_of_ship = 3
        self.hp = 30

    def change_pos(self, dx, dy):
        if 50 <= self.rect.x + dx * self.speed_of_ship <= WIDTH - self.width - 50:
            self.rect = self.rect.move(
                self.speed_of_ship * dx,
                self.speed_of_ship * dy
            )
        else:
            self.speed_of_ship *= -1


# --- Выстрел ---

# Выстрел врага
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
        for player in player_group:
            if pygame.sprite.collide_mask(self, player):
                if isinstance(self.parent_ship, EnemyLevelOne):
                    player.hp -= 1
                if isinstance(self.parent_ship, EnemyLevelTwo):
                    player.hp -= 2
                if isinstance(self.parent_ship, EnemyLevelThree):
                    player.hp -= 3
                if isinstance(self.parent_ship, EnemyLevelFour):
                    player.hp -= 4
                self.kill()
                return

        # Перемщение снаряда
        if self.rect.y + self.speed_of_shot <= HEIGHT + self.height:
            self.rect.y += self.speed_of_shot
        else:
            self.kill()
