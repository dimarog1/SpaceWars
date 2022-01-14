import json
import random

import sqlite3

import keyboard as keyboard
import pygame

from ProgramFiles.consts import *
from ProgramFiles.enemy_sprites import *
from ProgramFiles.player_sprites import *
from ProgramFiles.buttons import *
from itertools import cycle
from music.sounds import boom_sound, shoot_sound, btn_sound, fon_sound, selected_btn_sound, game_over_sound


def terminate():
    pygame.quit()
    exit(0)


def select_name_of_wave(level, wave):
    name = ''
    for elem in level:
        if level[elem] == wave:
            name = elem
    return name


pygame.init()
pygame.mixer.init()
SCREEN = pygame.display.set_mode(SIZE)

con = sqlite3.connect('settings.db')
cur = con.cursor()
cur1 = con.cursor()
cur2 = con.cursor()

loud = cur.execute("""SELECT music_sound, music_effects_sound FROM volume_values""")
bindings = cur1.execute("""SELECT Key_up, Key_down, Key_right, Key_left FROM key_bindings""")
ships_characteristic = cur2.execute("""SELECT price, size, damage FROM shop""")

loud_of_menu_music, loud_of_effects = map(float, *loud)
KEY_UP, KEY_DOWN, KEY_RIGHT, KEY_LEFT = map(int, *bindings)
ship1_characteristics, ship2_characteristics, ship3_characteristics = list(ships_characteristic)

first_bg = FirstBg()
second_bg = SecondBg()

GAME_TITLE_IMG = pygame.transform.scale(load_image('game_title.png', -1), (300, 200))

shoot_sound.set_volume(loud_of_effects)
boom_sound.set_volume(loud_of_effects)
game_over_sound.set_volume(loud_of_effects)
fon_sound.set_volume(loud_of_menu_music)
btn_sound.set_volume(loud_of_menu_music)
selected_btn_sound.set_volume(loud_of_menu_music)

dx = dy = 0


def keyboard_check(event):
    global dx, dy
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            if pause():
                menu()

    if event.type == pygame.KEYDOWN:
        if event.key == KEY_UP:
            dy += -1
        if event.key == KEY_DOWN:
            dy += 1
        if event.key == KEY_LEFT:
            dx += -1
        if event.key == KEY_RIGHT:
            dx += 1

    if event.type == pygame.KEYUP:
        if event.key == KEY_UP:
            dy += 1
        if event.key == KEY_DOWN:
            dy += -1
        if event.key == KEY_LEFT:
            dx += 1
        if event.key == KEY_RIGHT:
            dx += -1


def menu():
    enemy_level_two_img = pygame.transform.scale(load_image('enemy_level_two.png'), (90, 90))
    enemy_level_four_img = pygame.transform.scale(load_image('enemy_level_four.png'), (130, 130))

    background_enemies = [EnemyLevelFour(), EnemyLevelTwo(), EnemyLevelTwo(), EnemyLevelTwo(),
                          EnemyLevelTwo(), EnemyLevelTwo()]
    secret_enemy = SecretEnemy()
    secret_enemy.set_start_pos(350, 850)

    x = 125
    background_enemies[0].image = pygame.transform.rotate(enemy_level_four_img, 180)
    background_enemies[0].set_start_pos(110, 900)
    background_enemies[1].set_start_pos(x, 1100)
    background_enemies[2].set_start_pos(x, 1200)
    background_enemies[3].set_start_pos(x, 1300)
    background_enemies[4].set_start_pos(x, 1400)
    background_enemies[5].set_start_pos(x, 1500)

    count = 0
    font = pygame.font.SysFont('Jokerman', 48)
    clock = pygame.time.Clock()

    running = True

    play_btn = ClassicButton(font, 350, 240, 'Play')
    shop_btn = ClassicButton(font, 350, 310, 'Shop')
    settings_btn = ClassicButton(font, 350, 380, 'Settings')
    quit_btn = ClassicButton(font, 350, 450, 'Quit')

    fon_sound.play(-1)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()

        if play_btn.is_clicked():
            btn_sound.play()
            fon_sound.stop()
            for enemy in enemy_group:
                enemy.kill()
            main()

        if shop_btn.is_clicked():
            btn_sound.play()
            shop()

        if quit_btn.is_clicked():
            btn_sound.play()
            terminate()

        if settings_btn.is_clicked():
            btn_sound.play()
            settings()

        bg_group.draw(SCREEN)
        bg_group.update()

        for enemy in enemy_group:
            if not isinstance(enemy, SecretEnemy):
                enemy.rect.y += -3
            if isinstance(enemy, SecretEnemy) and count >= 10:
                enemy.rect.y += -1
            if isinstance(enemy, EnemyLevelTwo):
                enemy.image = pygame.transform.rotate(enemy_level_two_img, 180)
            if enemy.rect.y <= -enemy.rect.height:
                if isinstance(enemy, SecretEnemy):
                    count = 0
                    enemy.rect.x = 350
                if isinstance(enemy, EnemyLevelTwo):
                    enemy.rect.y = 840
                    count += 1
                else:
                    enemy.rect.y = 800
                if enemy.rect.x >= 450:
                    enemy.rect.x -= 500
                else:
                    if not isinstance(enemy, SecretEnemy):
                        enemy.rect.x += 500

        enemy_group.draw(SCREEN)
        SCREEN.blit(GAME_TITLE_IMG, (250, 50))

        play_btn.play_sound_if_btn_selected()
        shop_btn.play_sound_if_btn_selected()
        settings_btn.play_sound_if_btn_selected()
        quit_btn.play_sound_if_btn_selected()

        play_btn.render(SCREEN)
        shop_btn.render(SCREEN)
        settings_btn.render(SCREEN)
        quit_btn.render(SCREEN)

        clock.tick(FPS)
        pygame.display.flip()


def start_screen():
    pygame.display.set_caption(GAME_TITLE)

    clock = pygame.time.Clock()
    blink_event = pygame.USEREVENT + 0

    font = pygame.font.Font(None, 48)
    string_rendered = font.render("Press space key to start", True, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.center = SCREEN.get_rect().center
    intro_rect.top, intro_rect.x = 700, 200
    off_intro_text = pygame.Surface(intro_rect.size)
    off_intro_text.set_colorkey(0)
    blink_surfaces = cycle([string_rendered, off_intro_text])
    blink_surface = next(blink_surfaces)
    pygame.time.set_timer(blink_event, 800)
    SCREEN.blit(string_rendered, intro_rect)

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    btn_sound.play()
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if intro_rect.x < event.pos[0] < intro_rect.x + intro_rect.width\
                        and intro_rect.y < event.pos[1] < intro_rect.height + intro_rect.y:
                    btn_sound.play()
                    return
            elif event.type == blink_event:
                blink_surface = next(blink_surfaces)

        bg_group.draw(SCREEN)
        bg_group.update()

        SCREEN.blit(GAME_TITLE_IMG, (250, 50))
        SCREEN.blit(blink_surface, intro_rect)

        clock.tick(FPS)
        pygame.display.flip()


def settings():
    global KEY_UP, KEY_DOWN, KEY_RIGHT, KEY_LEFT, loud_of_menu_music, loud_of_effects

    clock = pygame.time.Clock()
    surface = pygame.Surface(SIZE)
    font = pygame.font.Font(None, 38)

    surface.fill((128, 128, 128))
    # это для того чтобы была иллюзия плавного перехода
    surface.set_alpha(50)

    back_btn = ClassicButton(font, 20, 750, 'Back')
    apply_btn = ClassicButton(font, 700, 750, 'Apply')

    pg_key = pygame.key

    music_sound_spinbox = SpinBox(400, 55, loud_of_menu_music)
    music_effects_sound_spinbox = SpinBox(400, 115, loud_of_effects)

    move_up_k = InputBox(400, 235, 300, 30, pg_key.name(KEY_UP))
    move_down_k = InputBox(400, 295, 300, 30, pg_key.name(KEY_DOWN))
    move_right_k = InputBox(400, 355, 300, 30, pg_key.name(KEY_RIGHT))
    move_left_k = InputBox(400, 415, 300, 30, pg_key.name(KEY_LEFT))
    keys = [move_up_k, move_down_k, move_right_k, move_left_k]

    display_text(surface, 'Sound', (WIDTH - 129) // 2, 10)
    display_text(surface, 'Menu music volume', 20, 60, 38)
    display_text(surface, 'Effects music volume', 20, 120, 38)

    display_text(surface, 'Controls', (WIDTH - 129) // 2, 180, 45)
    display_text(surface, 'Move forward', 20, 240, 38)
    display_text(surface, 'Move back', 20, 300, 38)
    display_text(surface, 'Move right', 20, 360, 38)
    display_text(surface, 'Move left', 20, 420, 38)

    is_running = True
    while is_running:
        SCREEN.blit(surface, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                else:
                    # изменение текста в rect
                    for key in keys:
                        key.update_text(event)

        if back_btn.is_clicked():
            btn_sound.play()
            return
        elif apply_btn.is_clicked():
            btn_sound.play()

            loud_of_menu_music = music_sound_spinbox.curr_value
            loud_of_effects = music_effects_sound_spinbox.curr_value

            cur.execute("""UPDATE volume_values
                                SET music_sound = ?""", (str(loud_of_menu_music),))
            cur.execute("""UPDATE volume_values
                                SET music_effects_sound = ?""", (str(loud_of_effects),))
            cur.execute("""UPDATE key_bindings
                                SET Key_up = ?""", (pg_key.key_code(move_up_k.text),))
            cur.execute("""UPDATE key_bindings
                                SET Key_down = ?""", (pg_key.key_code(move_down_k.text),))
            cur.execute("""UPDATE key_bindings
                                SET Key_left = ?""", (pg_key.key_code(move_left_k.text),))
            cur.execute("""UPDATE key_bindings
                                SET Key_right = ?""", (pg_key.key_code(move_right_k.text),))
            con.commit()

            shoot_sound.set_volume(loud_of_effects)
            boom_sound.set_volume(loud_of_effects)
            game_over_sound.set_volume(loud_of_effects)
            fon_sound.set_volume(loud_of_menu_music)
            btn_sound.set_volume(loud_of_menu_music)
            selected_btn_sound.set_volume(loud_of_menu_music)

            KEY_UP = pg_key.key_code(move_up_k.text)
            KEY_DOWN = pg_key.key_code(move_down_k.text)
            KEY_RIGHT = pg_key.key_code(move_right_k.text)
            KEY_LEFT = pg_key.key_code(move_left_k.text)
            return
        # Отрисовка
        music_sound_spinbox.render(surface)
        music_effects_sound_spinbox.render(surface)

        back_btn.play_sound_if_btn_selected()
        apply_btn.play_sound_if_btn_selected()

        back_btn.render(SCREEN)
        apply_btn.render(SCREEN)

        for key1 in keys:
            key1.update()
            key1.draw(surface, 7)
            key1.play_sound_if_btn_selected()

        clock.tick(FPS)
        pygame.display.flip()


def start_enemy_wave(wave, count):
    global dx, dy
    enemies_id = {
        1: EnemyLevelOne,
        2: EnemyLevelTwo,
        3: EnemyLevelThree,
        4: EnemyLevelFour,
    }
    ships_territory = 1 / len(wave)
    k = 0
    enemies = pygame.sprite.Group()
    L = 100
    R = 700
    for enemy_id in wave:
        enemy = enemies_id[enemy_id]()
        territory = (R - L) * ships_territory
        x = L + territory * k + (territory - enemy.width) // 2
        y = -150
        enemy.set_start_pos(x, y)
        enemies.add(enemy)
        k += 1
    tmp = 0
    while tmp < 200:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            keyboard_check(event)

        if player.alive():
            player.change_pos(dx, dy)

        for en in enemies:
            en.rect.y += 1
        tmp += 1
        bg_group.draw(SCREEN)
        bg_group.update()
        player_shots_group.update()
        enemy_shots_group.update()
        boom_group.update()

        # Удаление кораблей, если они уничтожены и проверка на их столкновение
        for enemy in enemy_group:
            enemy.check_alive()
            if pygame.sprite.collide_mask(player, enemy):
                player.hp -= 1
        for pl in player_group:
            pl.check_alive()

        clock.tick(FPS)

        # Отрисовка
        player_shots_group.draw(SCREEN)
        enemy_shots_group.draw(SCREEN)
        player_group.draw(SCREEN)
        enemy_group.draw(SCREEN)
        boom_group.draw(SCREEN)
        display_text(SCREEN, count, WIDTH // 2 - len(count) * 22, HEIGHT // 2 - 100, font_size=100, color=pygame.Color('red'))
        pygame.display.flip()
    return enemies


def main():
    global clock, player, dx, dy
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()

    # Загрузка уровня
    waves = list()
    with open(r'.\levels\level_one.json', 'r', encoding='utf-8') as level:
        level = json.loads(level.read())
    for wave in level:
        waves.append(level[wave])

    player = Player()
    # enemy1 = EnemyLevelFour()
    # enemy1.set_start_pos(109, 425)
    count = 1

    # Скорость выстрела (чем меньше число, тем больше скорость)
    player_speed_shooting = 20
    enemy_speed_shooting = 90
    a = 1000000

    # Выпуск корабля игрока
    while player.starting_ship():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        player.rect.y -= 1

        bg_group.draw(SCREEN)
        bg_group.update()
        clock.tick(FPS)

        # Отрисовка
        player_group.draw(SCREEN)
        enemy_group.draw(SCREEN)
        boom_group.draw(SCREEN)
        pygame.display.flip()

    name = select_name_of_wave(level, waves[0])
    enemies_of_wave = start_enemy_wave(waves[0], name)
    del waves[0]

    running = True

    while running:

        if len(enemies_of_wave) == 0:
            if len(waves) != 0:
                name = select_name_of_wave(level, waves[0])
                enemies_of_wave = start_enemy_wave(waves[0], name)
                del waves[0]
            else:
                running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keyboard_check(event)

        if count % player_speed_shooting == 0:
            # Вылет выстрела
            if player.alive():
                player_shot = PlayerProjectileLevelOne(player)
                shoot_sound.play()

        for enemy in enemy_group:
            if enemy.alive() and random.randint(0, enemy_speed_shooting + 100) == 1:
                enemy_shot = EnemyProjectile(enemy)
                shoot_sound.play()

        bg_group.draw(SCREEN)
        bg_group.update()

        # Удаление кораблей, если они уничтожены и проверка на их столкновение
        for enemy in enemy_group:
            enemy.check_alive()
            if pygame.sprite.collide_mask(player, enemy):
                player.hp = 0
        for pl in player_group:
            pl.check_alive()

        player_shots_group.update()
        enemy_shots_group.update()
        boom_group.update()

        if player.alive():
            player.change_pos(dx, dy)

        for enemy in enemy_group:
            enemy.change_pos(0, 0)

        clock.tick(FPS)

        # Отрисовка
        player_group.draw(SCREEN)
        enemies_of_wave.draw(SCREEN)
        player_shots_group.draw(SCREEN)
        enemy_shots_group.draw(SCREEN)
        boom_group.draw(SCREEN)
        pygame.display.flip()
        count += 1

        if not player.alive():
            game_over()

    pygame.mixer.quit()
    con.close()
    terminate()


def pause():
    surface = pygame.Surface(SIZE)
    surface.set_alpha(70)
    is_paused = True

    font = pygame.font.SysFont('Jokerman', 48)
    clock = pygame.time.Clock()

    resume_btn = ClassicButton(font, 320, 200, 'Continue')
    settings_btn = ClassicButton(font, 320, 270, 'Settings')
    back_to_menu_btn = ClassicButton(font, 320, 340, 'Back to menu')

    while is_paused:
        SCREEN.blit(surface, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_paused = False
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

        if resume_btn.is_clicked():
            btn_sound.play()
            return False

        if settings_btn.is_clicked():
            btn_sound.play()
            settings()

        if back_to_menu_btn.is_clicked():
            btn_sound.play()
            delete_all_sprites()
            pygame.time.delay(200)
            return True

        resume_btn.render(SCREEN)
        back_to_menu_btn.render(SCREEN)
        settings_btn.render(SCREEN)

        resume_btn.play_sound_if_btn_selected()
        settings_btn.play_sound_if_btn_selected()
        back_to_menu_btn.play_sound_if_btn_selected()

        pygame.display.flip()
        clock.tick(60)


# Отрисовка текста на экран
def display_text(surface, text, x, y, font_size=40, color=(255, 255, 255), draw_in_the_middle=False):
    font = pygame.font.Font(None, font_size)
    string = font.render(text, 1, color)
    if draw_in_the_middle:
        x = WIDTH // 2 - string.get_width() // 2
    surface.blit(string, (x, y))


def shop():
    shop_surface = pygame.Surface(SIZE)
    font_size = 30

    ship1 = pygame.transform.scale(load_image('player_from_shop1.png'), (100, 100))
    ship2 = pygame.transform.scale(load_image('player_from_shop2.png'), (100, 100))
    ship3 = pygame.transform.scale(load_image('player_from_shop3.png'), (70, 70))

    buy_btn = ShopButton(300, 700, 200, 20)

    rects = [AnimatedRect(50, 90, ship1.get_width() + 20, ship1.get_height() + 30),
             AnimatedRect(370, 90, ship2.get_width() + 20, ship2.get_height() + 30),
             AnimatedRect(665, 90, ship3.get_width() + 50, ship3.get_height() + 60)]

    shop_surface.blit(ship1, (60, 100))
    shop_surface.blit(ship2, (380, 100))
    shop_surface.blit(ship3, (690, 120))

    display_text(shop_surface, 'SCORE: {}', 600, 10)

    display_text(shop_surface, 'Price: {}'.format(ship1_characteristics[0]), 50, 250, font_size)
    display_text(shop_surface, 'Price: {}'.format(ship2_characteristics[0]), 370, 250, font_size)
    display_text(shop_surface, 'Price: {}'.format(ship3_characteristics[0]), 670, 250, font_size)
    display_text(shop_surface, 'Size: {}'.format(ship1_characteristics[1]), 50, 300, font_size)
    display_text(shop_surface, 'Size: {}'.format(ship2_characteristics[1]), 370, 300, font_size)
    display_text(shop_surface, 'Size: {}'.format(ship3_characteristics[1]), 670, 300, font_size)
    display_text(shop_surface, 'Damage: {}'.format(ship1_characteristics[2]), 50, 350, font_size)
    display_text(shop_surface, 'Damage: {}'.format(ship2_characteristics[2]), 370, 350, font_size)
    display_text(shop_surface, 'Damage {}'.format(ship3_characteristics[2]), 670, 350, font_size)

    is_running = True
    while is_running:
        SCREEN.blit(shop_surface, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        if buy_btn.is_clicked():
            for rect in rects:
                if rect.active:
                    btn_sound.play()
                    return

        for rect in rects:
            rect.update()
            rect.draw(shop_surface)

        buy_btn.render(SCREEN)
        buy_btn.play_sound_if_btn_selected()

        pygame.display.flip()


def game_over():
    game_over_surface = pygame.Surface(SIZE)
    game_over_surface.set_alpha(30)

    font = pygame.font.SysFont('Jokerman', 40)
    clock = pygame.time.Clock()

    retry_btn = ClassicButton(font, 340, 300, 'Retry')
    back_to_menu_btn = ClassicButton(font, 300, 360, 'Back to menu')
    is_running = True

    game_over_sound.play()
    display_text(game_over_surface, 'You`ve lost', 300, 100, 70, draw_in_the_middle=True)

    while is_running:
        SCREEN.blit(game_over_surface, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        if retry_btn.is_clicked():
            game_over_sound.stop()
            btn_sound.play()
            delete_all_sprites()
            main()

        if back_to_menu_btn.is_clicked():
            game_over_sound.stop()
            btn_sound.play()
            pygame.time.delay(200)
            delete_all_sprites()
            menu()

        retry_btn.play_sound_if_btn_selected()
        back_to_menu_btn.play_sound_if_btn_selected()

        retry_btn.render(SCREEN)
        back_to_menu_btn.render(SCREEN)

        clock.tick(FPS)
        pygame.display.flip()


def delete_all_sprites():
    for player_shot in player_shots_group:
        player_shot.kill()
    for enemy_shot in enemy_shots_group:
        enemy_shot.kill()
    for pl in player_group:
        pl.kill()
    for enemy in enemy_group:
        enemy.kill()
    for boom in boom_group:
        boom.kill()
