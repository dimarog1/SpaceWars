import json
import random

import sqlite3

import keyboard as keyboard

from ProgramFiles.consts import *
from ProgramFiles.enemy_sprites import *
from ProgramFiles.player_sprites import *
from ProgramFiles.buttons import *
from itertools import cycle
from music.sounds import boom_sound, shoot_sound, btn_sound, fon_sound


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

loud = cur.execute("""SELECT music_sound, music_effects_sound FROM volume_values""")
bindings = cur1.execute("""SELECT Key_up, Key_down, Key_right, Key_left FROM key_bindings""")

loud_of_menu_music, loud_of_effects = map(float, *loud)
KEY_UP, KEY_DOWN, KEY_RIGHT, KEY_LEFT = map(int, *bindings)

first_bg = FirstBg()
second_bg = SecondBg()

GAME_TITLE_IMG = pygame.transform.scale(load_image('game_title.png', -1), (300, 200))


shoot_sound.set_volume(loud_of_effects)
boom_sound.set_volume(loud_of_effects)
fon_sound.set_volume(loud_of_menu_music)
btn_sound.set_volume(loud_of_menu_music)

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
    # global X
    # enemy = Enemy()
    # background_enemies = [EnemyLevelOne((150, 900)), EnemyLevelOne((100, 1000)), EnemyLevelOne((150, 1100)),
    #                       EnemyLevelOne((100, 1200)), EnemyLevelOne((150, 1300)), EnemyLevelOne((100, 1400))]
    # 391
    # 342
    # 682
    pygame.mixer.init()
    font = pygame.font.SysFont('Jokerman', 48)
    clock = pygame.time.Clock()

    running = True

    play_btn = Button(font, 350, 240, 'Play')
    shop_btn = Button(font, 350, 310, 'Shop')
    settings_btn = Button(font, 350, 380, 'Settings')
    quit_btn = Button(font, 350, 450, 'Quit')

    fon_sound.play(-1)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()

        if play_btn.is_clicked():
            fon_sound.stop()
            btn_sound.play()
            # for enemy in enemy_group:
            #     enemy.kill()
            main()

        if quit_btn.is_clicked():
            btn_sound.play()
            pygame.time.delay(200)
            terminate()

        if settings_btn.is_clicked():
            btn_sound.play()
            settings()

        bg_group.draw(SCREEN)
        bg_group.update()

        # for enemy in enemy_group:
        #     enemy.change_pos(0, -2)
        #     if enemy.rect.y <= -enemy.rect.height:
        #         # X = random.randint(50, 680)
        #         enemy.rect.y = 850
        #         enemy.rect.x += 100
        #     if enemy.rect.x >= 600:
        #         enemy.rect.x = 100
                # print(X)
            # if enemy.rect.x >= 250 or enemy.rect.x >= 200:
            #     enemy.rect.x -= 100
            # else:
            #     enemy.rect.x -= 100

        enemy_group.draw(SCREEN)
        SCREEN.blit(GAME_TITLE_IMG, (250, 50))

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
                    pygame.mixer.quit()
                    menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if intro_rect.x < event.pos[0] < intro_rect.x + intro_rect.width\
                        and intro_rect.y < event.pos[1] < intro_rect.height + intro_rect.y:
                    menu()
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
    # surface.set_alpha(30)

    back_btn = Button(font, 20, 750, 'Back')
    apply_btn = Button(font, 700, 750, 'Apply')

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
            return
        elif apply_btn.is_clicked():
            cur.execute("""UPDATE volume_values
                                SET music_sound = ?""", (str(music_sound_spinbox.curr_value),))
            cur.execute("""UPDATE volume_values
                                SET music_effects_sound = ?""", (str(music_effects_sound_spinbox.curr_value),))
            cur.execute("""UPDATE key_bindings
                                SET Key_up = ?""", (pg_key.key_code(move_up_k.text),))
            cur.execute("""UPDATE key_bindings
                                SET Key_down = ?""", (pg_key.key_code(move_down_k.text),))
            cur.execute("""UPDATE key_bindings
                                SET Key_left = ?""", (pg_key.key_code(move_left_k.text),))
            cur.execute("""UPDATE key_bindings
                                SET Key_right = ?""", (pg_key.key_code(move_right_k.text),))
            con.commit()

            loud_of_menu_music = music_sound_spinbox.curr_value
            loud_of_effects = music_effects_sound_spinbox.curr_value

            shoot_sound.set_volume(loud_of_effects)
            boom_sound.set_volume(loud_of_effects)
            fon_sound.set_volume(loud_of_menu_music)
            btn_sound.set_volume(loud_of_menu_music)

            KEY_UP = pg_key.key_code(move_up_k.text)
            KEY_DOWN = pg_key.key_code(move_down_k.text)
            KEY_RIGHT = pg_key.key_code(move_right_k.text)
            KEY_LEFT = pg_key.key_code(move_left_k.text)

        # Отрисовка
        music_sound_spinbox.render(surface, font)
        music_effects_sound_spinbox.render(surface, font)

        back_btn.render(surface)
        apply_btn.render(surface)

        for key1 in keys:
            key1.update()
            key1.draw(surface, 7)

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
    player_speed_shooting = 15
    enemy_speed_shooting = 90

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
                player.hp -= 1
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

    pygame.mixer.quit()
    con.close()
    terminate()


def pause():
    surface = pygame.Surface(SIZE)
    surface.set_alpha(100)
    is_paused = True

    font = pygame.font.Font(None, 40)
    clock = pygame.time.Clock()

    resume_btn = Button(font, 340, 300, 'Continue')
    back_to_menu_btn = Button(font, 340, 350, 'Back to menu')

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
            return False

        if back_to_menu_btn.is_clicked():
            for player_shot in player_shots_group:
                player_shot.kill()
            for enemy_shot in enemy_shots_group:
                enemy_shot.kill()
            for player in player_group:
                player.kill()
            for enemy in enemy_group:
                enemy.kill()
            pygame.time.delay(200)
            return True

        resume_btn.render(surface)
        back_to_menu_btn.render(surface)

        pygame.display.flip()
        clock.tick(60)


# Отрисовка текста на экран
def display_text(surface, text, x, y, font_size=40, color=(255, 255, 255)):
    font = pygame.font.Font(None, font_size)
    string = font.render(text, 1, color)
    surface.blit(string, (x, y))
