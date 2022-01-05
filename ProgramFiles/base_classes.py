import os
from music.sounds import boom_sound

from ProgramFiles.consts import *


pygame.mixer.init()

# !!! SPRITES GROUPS !!!
all_sprites = pygame.sprite.Group()

player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

all_shots_group = pygame.sprite.Group()
player_shots_group = pygame.sprite.Group()
enemy_shots_group = pygame.sprite.Group()

hp_bar_group = pygame.sprite.Group()

boom_group = pygame.sprite.Group()

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


class Ship(pygame.sprite.Sprite):
    def __init__(self, screen, position):
        super().__init__(all_sprites)
        self.screen = screen
        self.image = pygame.transform.scale(load_image('player.png'), (100, 100))
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect().move(*position)
        self.speed_of_ship = 5
        self.hp = 1

    def change_pos(self, dx, dy):
        if 0 <= self.rect.x + dx * self.speed_of_ship <= WIDTH - self.width and \
                self.height <= self.rect.y + dy * self.speed_of_ship + self.height <= HEIGHT:
            self.rect = self.rect.move(
                self.speed_of_ship * dx,
                self.speed_of_ship * dy
            )

    def check_alive(self):
        # Проверяем количство hp
        if self.hp <= 0:
            self.kill()
            boom = BoomSprite(self)
            boom_sound.play()

    def __str__(self):
        return f'{self.rect.x}, {self.rect.y}'

    def __repr__(self):
        return f'{self.rect.x}, {self.rect.y}'


# Выстрел
class Projectile(pygame.sprite.Sprite):
    def __init__(self, parent_ship):
        super().__init__(all_sprites)
        self.parent_ship = parent_ship
        self.image = pygame.transform.scale(load_image('shot.png'), (20, 30))
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect().move(
            self.parent_ship.rect.x + self.parent_ship.width // 2 - self.width // 2,
            self.parent_ship.rect.y - self.height
        )
        self.speed_of_shot = 10


# Анимация взрыва
class BoomSprite(pygame.sprite.Sprite):
    def __init__(self, parent):
        super().__init__(boom_group)
        self.parent = parent
        self.sheet = load_image('boom.png')
        self.columns = 8
        self.rows = 6
        self.frames = []
        self.cut_sheet(self.sheet, self.columns, self.rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(parent.rect.x, parent.rect.y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.cur_frame + 1 < self.columns * self.rows:
            self.cur_frame += 1
            self.image = pygame.transform.scale(self.frames[self.cur_frame], (self.parent.width, self.parent.height))
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
