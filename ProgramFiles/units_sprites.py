import os
from ProgramFiles.consts import *


# !!! SPRITES GROUPS !!!
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_shots_group = pygame.sprite.Group()
bg_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('images\\', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        exit(0)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# Игрок
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group)
        self.image = pygame.transform.scale(load_image('player.png'), (100, 100))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect().move(WIDTH // 2 - self.width // 2, HEIGHT - 130)
        self.speed_of_ship = 5

    def change_pos(self, dx, dy):
        if 0 <= self.rect.x + dx * self.speed_of_ship <= WIDTH - self.width and \
                self.height <= self.rect.y + dy * self.speed_of_ship + self.height <= HEIGHT:
            self.rect = self.rect.move(
                self.speed_of_ship * dx,
                self.speed_of_ship * dy
            )


# Враг первого уровня
class EnemyLevelOne(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(enemy_group)
        self.image = pygame.transform.scale(load_image('enemy_level_one.png'), (100, 100))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect().move(WIDTH // 2 - self.width // 2, 130)
        self.speed_of_ship = 5

    def change_pos(self, dx, dy):
        if 0 <= self.rect.x + dx * self.speed_of_ship <= WIDTH - self.width and \
                self.height <= self.rect.y + dy * self.speed_of_ship + self.height <= HEIGHT:
            self.rect = self.rect.move(
                self.speed_of_ship * dx,
                self.speed_of_ship * dy
            )


# Выстрел
class ProjectileLevelOne(pygame.sprite.Sprite):
    def __init__(self, parent_ship):
        super().__init__(player_shots_group)
        self.parent_ship = parent_ship
        self.image = pygame.transform.scale(load_image('shot.png'), (20, 30))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect().move(
            self.parent_ship.rect.x + self.parent_ship.width // 2 - self.width // 2,
            self.parent_ship.rect.y - self.height
        )
        self.speed_of_shot = 10

    def update(self):
        if self.rect.y - self.speed_of_shot >= 0 - self.height:
            self.rect.y -= self.speed_of_shot
        else:
            self.kill()


# Первый бг
class FirstBg(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(bg_group)
        self.image = load_image('background1.jpg')
        self.rect = self.image.get_rect().move(0, 0)
        self.speed = 3

    def update(self):
        if self.rect.y + self.speed >= HEIGHT:
            self.rect = self.image.get_rect().move(0, -800)
        else:
            self.rect.y += self.speed


# Второй бг
class SecondBg(FirstBg):
    def __init__(self):
        super().__init__()
        self.image = load_image('background2.jpg')
        self.rect = self.image.get_rect().move(0, -800)
