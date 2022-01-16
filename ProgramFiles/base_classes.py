import os
from music.sounds import boom_sound, selected_btn_sound, gained_bonus_sound

from ProgramFiles.consts import *


pygame.mixer.init()

# !!! SPRITES GROUPS !!!

# Все спрайты
all_sprites = pygame.sprite.Group()

# Группы игрока и врагов
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# Сердечки
hearts_group = pygame.sprite.Group()

# Группы выстрелов
all_shots_group = pygame.sprite.Group()
player_shots_group = pygame.sprite.Group()
enemy_shots_group = pygame.sprite.Group()

# Группа усилений
gains_group = pygame.sprite.Group()

# Щит
shield_group = pygame.sprite.Group()

# Группа взрывов
boom_group = pygame.sprite.Group()

# Группа заднего фона
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

    def set_angle_of_projectile(self, angle):
        self.image = pygame.transform.rotate(self.image, 30)
        self.mask = pygame.mask.from_surface(self.image)


# Усиление
class Gain(pygame.sprite.Sprite):
    def __init__(self, parent_ship):
        super().__init__(gains_group)
        self.parent_ship = parent_ship
        self.image = pygame.transform.scale(load_image('shot.png'), (40, 40))
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect().move(
            self.parent_ship.rect.x + (self.parent_ship.width - self.width) // 2,
            self.parent_ship.rect.y + (self.parent_ship.height - self.height) // 2,
        )
        self.speed = 2

    def improve(self, player):
        pass

    def update(self):
        for player in player_group:
            if pygame.sprite.collide_mask(self, player):
                gained_bonus_sound.play()
                self.improve(player)
                self.kill()
                return

        # Перемщение снаряда
        if self.rect.y + self.speed <= HEIGHT + self.height:
            self.rect.y += self.speed
        else:
            self.kill()


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


# кнопки
class Button:
    def __init__(self, x, y, color_of_article=(0, 255, 0), color_of_selected_article=(255, 0, 0)):
        self.x, self.y = x, y
        self.color_of_article, self.color_of_selected_article = color_of_article, color_of_selected_article

    def is_selected(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.x < mouse_pos[0] < self.x + self.off_string.get_width() \
                and self.y < mouse_pos[1] < self.y + self.off_string.get_height():
            return True
        return False

    def play_sound_if_btn_selected(self):
        if self.is_selected():
            if self.selected:
                selected_btn_sound.play()
                self.selected = False
        else:
            self.selected = True

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_btn_clicked = pygame.mouse.get_pressed()
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + 70 and mouse_btn_clicked[0] == 1:
            return True
        return False


class BoxAndRect:
    def __init__(self, x, y, w, h, active_color=(255, 0, 0), inactive_color=(0, 255, 0)):
        self.x, self.y = x, y
        self.width, self.height = w, h
        self.active_color, self.inactive_color = active_color, inactive_color
