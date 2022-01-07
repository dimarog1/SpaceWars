from ProgramFiles.base_classes import *


# Игрок
class Player(Ship, pygame.sprite.Sprite):
    def __init__(self, screen, position=(0, 0)):
        Ship.__init__(self, screen, position)
        pygame.sprite.Sprite.__init__(self, player_group)
        self.image = pygame.transform.scale(load_image('player.png'), (100, 100))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(WIDTH // 2 - self.width // 2, HEIGHT + 10)
        self.speed_of_shooting = 30
        self.projectiles = (PlayerProjectileLevelOne, PlayerProjectileLevelTwo,
                            PlayerProjectileLevelThree, PlayerProjectileLevelFour)
        self.level_of_projectiles = 1
        self.projectile = self.projectiles[self.level_of_projectiles - 1]

    def starting_ship(self):
        if self.rect.y >= HEIGHT - 130:
            return True
        return False

    def spawn_shield(self):
        if len(shield_group) < 1:
            shield = Shield(self)


# Улучшение снарядов
class ShotRangeGain(Gain):
    def __init__(self, parent_ship):
        Gain.__init__(self, parent_ship)
        self.image = pygame.transform.scale(load_image('projectile_gain.png'), (40, 40))
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect().move(
            self.parent_ship.rect.x + (self.parent_ship.width - self.width) // 2,
            self.parent_ship.rect.y + (self.parent_ship.height - self.height) // 2,
        )

    def improve(self, player):
        if player.level_of_projectiles < 4:
            player.level_of_projectiles += 1
            player.projectile = player.projectiles[player.level_of_projectiles - 1]


# Увличение скорости снарядов
class ShotSpeedGain(Gain):
    def __init__(self, parent_ship):
        Gain.__init__(self, parent_ship)
        self.image = pygame.transform.scale(load_image('speed_of_shooting_gain.png'), (40, 40))
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect().move(
            self.parent_ship.rect.x + (self.parent_ship.width - self.width) // 2,
            self.parent_ship.rect.y + (self.parent_ship.height - self.height) // 2,
        )
        self.speed_up = -5

    def improve(self, player):
        if player.speed_of_shooting + self.speed_up >= 10:
            player.speed_of_shooting += self.speed_up


# Щит
class ShieldGain(Gain):
    def __init__(self, parent_ship):
        Gain.__init__(self, parent_ship)
        self.image = pygame.transform.scale(load_image('shield_gain.png'), (40, 40))
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect().move(
            self.parent_ship.rect.x + (self.parent_ship.width - self.width) // 2,
            self.parent_ship.rect.y + (self.parent_ship.height - self.height) // 2,
        )

    def improve(self, player):
        player.spawn_shield()


class Shield(pygame.sprite.Sprite):
    def __init__(self, parent_ship):
        super().__init__(shield_group)
        self.parent_ship = parent_ship
        self.image = pygame.transform.scale(load_image('shield.png'), (120, 120))
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect().move(
            self.parent_ship.rect.x,
            self.parent_ship.rect.y,
        )
        self.hp = 1

    def update(self):
        if self.hp <= 0:
            self.kill()
            return

        self.rect.x = self.parent_ship.rect.x - 10
        self.rect.y = self.parent_ship.rect.y - 10


# Выстрел игрока
class PlayerProjectile(Projectile, pygame.sprite.Sprite):
    def __init__(self, parent_ship):
        Projectile.__init__(self, parent_ship)
        pygame.sprite.Sprite.__init__(self, player_shots_group)
        self.image = pygame.transform.scale(load_image('shot.png'), (17, 27))
        self.damage = 10

    def update(self):
        # Столкновения с кораблём
        for enemy in enemy_group:
            if pygame.sprite.collide_mask(self, enemy):
                enemy.activate_hp_bar()
                enemy.hp -= self.damage
                self.kill()
                return

        # Перемщение снаряда
        if self.rect.y - self.speed_of_shot >= 0 - self.height:
            self.rect.y -= self.speed_of_shot
        else:
            self.kill()


# Выстрел игрока 1 lvl
class PlayerProjectileLevelOne(PlayerProjectile):
    def __init__(self, parent_ship):
        PlayerProjectile.__init__(self, parent_ship)
        self.image = pygame.transform.scale(load_image('shot.png'), (17, 27))
        self.mask = pygame.mask.from_surface(self.image)
        self.damage = 10


# Выстрел игрока 2 lvl
class PlayerProjectileLevelTwo(PlayerProjectile):
    def __init__(self, parent_ship):
        PlayerProjectile.__init__(self, parent_ship)
        self.image = pygame.transform.scale(load_image('shot_level_two.png'), (40, 30))
        self.image = pygame.transform.rotate(self.image, 180)
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect().move(
            self.parent_ship.rect.x + self.parent_ship.width // 2 - self.width // 2,
            self.parent_ship.rect.y - self.height
        )
        self.damage = 15


# Выстрел игрока 3 lvl
class PlayerProjectileLevelThree(PlayerProjectile):
    def __init__(self, parent_ship):
        PlayerProjectile.__init__(self, parent_ship)
        self.image = pygame.transform.scale(load_image('shot_level_three.png'), (70, 40))
        self.image = pygame.transform.rotate(self.image, 180)
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect().move(
            self.parent_ship.rect.x + self.parent_ship.width // 2 - self.width // 2,
            self.parent_ship.rect.y - self.height
        )
        self.damage = 20


# Выстрел игрока 4 lvl
class PlayerProjectileLevelFour(PlayerProjectile):
    def __init__(self, parent_ship):
        PlayerProjectile.__init__(self, parent_ship)
        self.image = pygame.transform.scale(load_image('shot_level_four.png'), (110, 70))
        self.image = pygame.transform.rotate(self.image, 180)
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect().move(
            self.parent_ship.rect.x + self.parent_ship.width // 2 - self.width // 2,
            self.parent_ship.rect.y - self.height
        )
        self.damage = 25
