import json
import sqlite3
import sys
from itertools import cycle

import pygame.font
import stats as stats

from ProgramFiles.buttons import *
from ProgramFiles.enemy_sprites import *
from ProgramFiles.player_sprites import *
from music.sounds import boom_sound, shoot_sound, btn_sound, fon_sound, selected_btn_sound, game_over_sound, boss_second_attack_sound


def terminate():
    pygame.quit()
    sys.exit(0)


def select_name_of_wave(level, wave):
    name = ''
    for elem in level:
        if level[elem] == wave:
            name = elem
    return name


def move_enemies(enemies):
    for enemy in enemies:
        if isinstance(enemy, Boss):
            return
    on_screen = True
    for enemy in enemies:
        if not enemy.check_is_ship_on_screen():
            on_screen = False
    if on_screen:
        enemies.update()
    else:
        for enemy in enemies:
            enemy.speed_of_ship *= -1


pygame.init()
pygame.mixer.init()
SCREEN = pygame.display.set_mode(SIZE)

con = sqlite3.connect('settings.db')
cur = con.cursor()

loudness = cur.execute("""SELECT music_sound, music_effects_sound FROM volume_values""")
bindings = con.cursor().execute("""SELECT Key_up, Key_down, Key_right, Key_left FROM key_bindings""")
player_stats = con.cursor().execute("""SELECT size, damage, speed_of_shooting,
                                    speed_of_ship, hp, luck, image FROM current_ship_stats""")
ships_characteristic = con.cursor().execute("""SELECT size, damage, speed_of_shooting, speed_of_ship, 
                                                hp, luck, price FROM shop""")

SCORE = con.cursor().execute("""SELECT SCORE FROM score""")
SCORE = list(*SCORE)[0]
player_stats = list(*player_stats)

purchased_ships_data = con.cursor().execute("""SELECT image FROM purchased_ships""")
purchased_ships = []
for i in purchased_ships_data:
    purchased_ships.append(i[0])
print(purchased_ships)

loud_of_menu_music, loud_of_effects = map(float, *loudness)
KEY_UP, KEY_DOWN, KEY_RIGHT, KEY_LEFT = map(int, *bindings)
ship1_characteristics, ship2_characteristics, ship3_characteristics, ship4_characteristics = list(ships_characteristic)

first_bg = FirstBg()
second_bg = SecondBg()

GAME_TITLE_IMG = pygame.transform.scale(load_image('game_title.png', -1), (300, 200))
BACKGROUND_FON = pygame.transform.scale(load_image('background1.jpg'), (800, 800))

shoot_sound.set_volume(loud_of_effects)
boom_sound.set_volume(loud_of_effects)
game_over_sound.set_volume(loud_of_effects)
gained_bonus_sound.set_volume(loud_of_effects)
boss_second_attack_sound.set_volume(loud_of_effects)
fon_sound.set_volume(loud_of_menu_music)
btn_sound.set_volume(loud_of_menu_music)
selected_btn_sound.set_volume(loud_of_menu_music)


dx, dy = 0, 0
k_up_clicked = False
k_right_clicked = False
k_down_clicked = False
k_left_clicked = False


def keyboard_check(event):
    global dx, dy, k_up_clicked, k_right_clicked, k_down_clicked, k_left_clicked
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            if pause():
                menu()

    if event.type == pygame.KEYDOWN:
        if event.key == KEY_UP:
            dy += -1
            k_up_clicked = True
        if event.key == KEY_DOWN:
            dy += 1
            k_down_clicked = True
        if event.key == KEY_LEFT:
            dx += -1
            k_left_clicked = True
        if event.key == KEY_RIGHT:
            dx += 1
            k_right_clicked = True

    if event.type == pygame.KEYUP:
        if event.key == KEY_UP and k_up_clicked:
            dy += 1
            k_up_clicked = False
        if event.key == KEY_DOWN and k_down_clicked:
            dy += -1
            k_down_clicked = False
        if event.key == KEY_LEFT and k_left_clicked:
            dx += 1
            k_left_clicked = False
        if event.key == KEY_RIGHT and k_right_clicked:
            dx += -1
            k_right_clicked = False


def menu():
    enemy_level_two_img = pygame.transform.scale(load_image('enemy_level_two.png'), (90, 90))
    enemy_level_four_img = pygame.transform.scale(load_image('enemy_level_four.png'), (130, 130))

    background_enemies = [EnemyLevelFour(SCREEN, Player), EnemyLevelTwo(SCREEN, Player), EnemyLevelTwo(SCREEN, Player), EnemyLevelTwo(SCREEN, Player),
                          EnemyLevelTwo(SCREEN, Player), EnemyLevelTwo(SCREEN, Player)]
    secret_enemy = SecretEnemy(SCREEN, Player)
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
            pygame.time.delay(200)
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
    font = pygame.font.SysFont('Jokerman', 38)

    surface.fill((128, 128, 128))
    # это для того чтобы была иллюзия плавного перехода
    surface.set_alpha(50)

    back_btn = ClassicButton(font, 20, 730, 'Back')
    apply_btn = ClassicButton(font, 680, 730, 'Apply')

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
                    btn_sound.play()
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
            gained_bonus_sound.set_volume(loud_of_effects)
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


def start_player_ship():
    clock = pygame.time.Clock()
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
        hearts_group.draw(SCREEN)
        pygame.display.flip()


def start_enemy_wave(wave, count):
    global dx, dy
    clock = pygame.time.Clock()
    enemies_id = {
        1: EnemyLevelOne,
        2: EnemyLevelTwo,
        3: EnemyLevelThree,
        4: EnemyLevelFour,
        "boss": Boss
    }
    ships_territory = 1 / len(wave)
    k = 0
    enemies = pygame.sprite.Group()
    L = 100
    R = 700
    for enemy_info in wave:
        if enemy_info != 0:
            enemy = enemies_id[enemy_info](SCREEN, player)
            territory = (R - L) * ships_territory
            x = L + territory * k + (territory - enemy.width) // 2
            y = -150
            enemy.set_start_pos(x, y)
            enemies.add(enemy)
            enemy.shooting = bool(k % 2)
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
        shield_group.update()
        gains_group.update()
        boom_group.update()

        # Удаление кораблей, если они уничтожены и проверка на их столкновение
        for enemy_info in enemy_group:
            enemy_info.check_alive()
            if pygame.sprite.collide_mask(player, enemy_info):
                player.hp -= 1
        for pl in player_group:
            pl.check_alive()

        clock.tick(FPS)

        # Отрисовка
        player_shots_group.draw(SCREEN)
        enemy_shots_group.draw(SCREEN)
        player_group.draw(SCREEN)
        enemy_group.draw(SCREEN)
        shield_group.draw(SCREEN)
        boom_group.draw(SCREEN)
        gains_group.draw(SCREEN)
        display_text(SCREEN, count, WIDTH // 2 - len(count) * 22,
                     HEIGHT // 2 - 100, font_size=100, color=pygame.Color('red'))
        hearts_group.draw(SCREEN)
        pygame.display.flip()
    return enemies


def replace_ship(ship, change_y):
    clock = pygame.time.Clock()
    condition = True

    while condition:
        if change_y < 0:
            condition = ship.rect.y >= -ship.height - 30
        else:
            condition = ship.rect.y <= 70

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            keyboard_check(event)

        if player.alive():
            player.change_pos(dx, dy)

        ship.rect.y += change_y
        bg_group.draw(SCREEN)
        bg_group.update()
        player_shots_group.update()
        enemy_shots_group.update()
        shield_group.update()
        gains_group.update()
        boom_group.update()

        # Удаление кораблей, если они уничтожены и проверка на их столкновение
        for enemy_info in enemy_group:
            enemy_info.check_alive()
            if pygame.sprite.collide_mask(player, enemy_info):
                player.hp -= 1
        for pl in player_group:
            pl.check_alive()

        clock.tick(FPS)

        # Отрисовка
        player_group.draw(SCREEN)
        gains_group.draw(SCREEN)
        enemy_group.draw(SCREEN)
        player_shots_group.draw(SCREEN)
        enemy_shots_group.draw(SCREEN)
        shield_group.draw(SCREEN)
        gains_group.update()
        boom_group.draw(SCREEN)
        hearts_group.draw(SCREEN)
        pygame.display.flip()


def third_boss_attack(enemy_reinforcement, enemy, count):
    if len(enemy_reinforcement) == 0:
        enemy.doing_third_attack = False
        replace_ship(enemy, 2)
        enemy.choose_attack()
    move_enemies(enemy_reinforcement)
    for unit in enemy_reinforcement:
        unit.check_alive()
        if pygame.sprite.collide_mask(player, unit):
            player.hp -= 1
        if count % unit.speed_of_shooting == 0:
            if unit.alive() and unit.shooting:
                unit.shoot()
                unit.shooting = False
                shoot_sound.play()
            elif not unit.shooting:
                unit.shooting = True
        unit.draw_hp_bar()
    enemy_reinforcement.draw(SCREEN)
    hearts_group.draw(SCREEN)


def main():
    global player, dx, dy, SCORE
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()

    # Загрузка уровня
    waves = list()
    with open(r'.\levels\level_one.json', 'r', encoding='utf-8') as level:
        level = json.loads(level.read())
    for wave in level:
        if wave != "SCORE":
            waves.append(level[wave])
        else:
            SCORE = level[wave]

    player = Player(SCREEN, *player_stats)
    count = 1

    # Выпуск корабля игрока
    start_player_ship()

    name_of_wave = select_name_of_wave(level, waves[0])
    enemies_of_wave = start_enemy_wave(waves[0], name_of_wave)
    del waves[0]

    running = True

    while running:

        if len(enemies_of_wave) == 0:
            if len(waves) != 0:
                name_of_wave = select_name_of_wave(level, waves[0])
                enemies_of_wave = start_enemy_wave(waves[0], name_of_wave)
                del waves[0]
            else:
                cur.execute("""UPDATE score
                                        SET SCORE = ?""", (SCORE,))
                con.commit()
                running = False

        # Передвижение игрока и врагов
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keyboard_check(event)
        move_enemies(enemies_of_wave)

        # Вылет выстрела
        if player.alive() and count % player.speed_of_shooting == 0:
            player_shot = player.projectile(player)
            shoot_sound.play()

        bg_group.draw(SCREEN)
        bg_group.update()

        for enemy in enemy_group:
            if isinstance(enemy, Boss):
                part1 = int(enemy.max_hp * 0.75)
                part2 = int(enemy.max_hp * 0.50)
                part3 = int(enemy.max_hp * 0.25)
                if enemy.hp in range(part1 - 50, part1) \
                        or enemy.hp in range(part2 - 50, part2) \
                        or enemy.hp in range(part3 - 50, part3):
                    enemy.attack_type = 3
                    enemy.plug = 1
                    enemy.hp -= 50
                    enemy.doing_third_attack = True
                    replace_ship(enemy, -2)
                    enemy_reinforcement = start_enemy_wave(enemy.third_attack(), "ПОДКРЕПЛЕНИЕ")

                if count % enemy.attack_intervals == 0 and not enemy.doing_third_attack:
                    if enemy.plug == 0:
                        enemy.choose_attack()
                    else:
                        enemy.plug = 0

                if enemy.attack_type == 3:
                    third_boss_attack(enemy_reinforcement, enemy, count)
                else:
                    enemy.attack(count)
                break
            if count % enemy.speed_of_shooting == 0:
                if enemy.alive() and enemy.shooting:
                    enemy.shoot()
                    enemy.shooting = False
                    shoot_sound.play()
                elif not enemy.shooting:
                    enemy.shooting = True

        # Удаление кораблей, если они уничтожены и проверка на их столкновение
        for enemy in enemy_group:
            enemy.check_alive()
            if pygame.sprite.collide_mask(player, enemy):
                player.reduce_hp()
        for pl in player_group:
            pl.check_alive()

        player_shots_group.update()
        enemy_shots_group.update()
        boom_group.update()

        if player.alive():
            player.change_pos(dx, dy)
        shield_group.update()

        clock.tick(FPS)

        # Отрисовка
        player_group.draw(SCREEN)
        enemies_of_wave.draw(SCREEN)
        for unit in enemies_of_wave:
            unit.draw_hp_bar()
        gains_group.draw(SCREEN)
        player_shots_group.draw(SCREEN)
        enemy_shots_group.draw(SCREEN)
        shield_group.draw(SCREEN)
        gains_group.update()
        boom_group.draw(SCREEN)
        hearts_group.draw(SCREEN)
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
                    btn_sound.play()
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
    global player_stats, SCORE, purchased_ships
    shop_surface = pygame.Surface(SIZE)
    shop_surface.blit(BACKGROUND_FON, (0, 0))
    font_size = 30

    ship1 = pygame.transform.scale(load_image('player.png'), (100, 100))
    ship2 = pygame.transform.scale(load_image('player_from_shop1.png'), (100, 100))
    ship3 = pygame.transform.scale(load_image('player_from_shop2.png'), (100, 100))
    ship4 = pygame.transform.scale(load_image('player_from_shop3.png'), (70, 70))

    buy_btn = ShopButton(50, 700, 200, 20)
    select_btn = ShopButton(500, 700, 250, 20, text='Select')

    rects = [AnimatedRect(50, 90, ship2.get_width() + 20, ship1.get_height() + 30, 0),
             AnimatedRect(240, 90, ship2.get_width() + 20, ship2.get_height() + 30, 1),
             AnimatedRect(430, 90, ship3.get_width() + 20, ship3.get_height() + 30, 2),
             AnimatedRect(610, 90, ship4.get_width() + 50, ship4.get_height() + 60, 3)]

    shop_surface.blit(ship1, (60, 100))
    shop_surface.blit(ship2, (250, 100))
    shop_surface.blit(ship3, (440, 100))
    shop_surface.blit(ship4, (635, 120))

    display_text(shop_surface, 'SCORE: {}'.format(SCORE), 600, 10)

    titles = ['Size', 'Damage', 'Shots speed', 'Ship speed', 'HP', 'Luck', 'Price']
    for i in range(len(ship1_characteristics)):

        display_text(shop_surface, f'{titles[i]}: {ship1_characteristics[i]}', 50, 250 + i * 50, font_size)
        display_text(shop_surface, f'{titles[i]}: {ship2_characteristics[i]}', 240, 250 + i * 50, font_size)
        display_text(shop_surface, f'{titles[i]}: {ship3_characteristics[i]}', 430, 250 + i * 50, font_size)
        display_text(shop_surface, f'{titles[i]}: {ship4_characteristics[i]}', 610, 250 + i * 50, font_size)

    is_running = True
    while is_running:
        SCREEN.blit(shop_surface, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                btn_sound.play()
                return

        if buy_btn.is_clicked():
            for rect in rects:
                if rect.active:
                    if rect.id == 1 and SCORE >= 200 and 'player_from_shop1.png' not in purchased_ships:
                        purchased_ships.append('player_from_shop1.png')
                        btn_sound.play()
                        player_stats[:-1] = ship2_characteristics[:-1]
                        player_stats[-1] = 'player_from_shop1.png'
                        SCORE -= ship2_characteristics[-1]
                        cur.execute("""UPDATE score SET SCORE = ?""", (SCORE,))
                        cur.execute("""INSERT INTO purchased_ships(image) VALUES(?)""", (player_stats[-1],))
                        con.commit()
                        return
                    if rect.id == 2 and SCORE >= 400 and 'player_from_shop2.png' not in purchased_ships:
                        purchased_ships.append('player_from_shop2.png')
                        btn_sound.play()
                        player_stats[:-1] = ship3_characteristics[:-1]
                        player_stats[-1] = 'player_from_shop2.png'
                        SCORE -= ship3_characteristics[-1]
                        cur.execute("""UPDATE score SET SCORE = ?""", (SCORE,))
                        cur.execute("""INSERT INTO purchased_ships(image) VALUES(?)""", (player_stats[-1],))
                        con.commit()
                        return
                    if rect.id == 3 and SCORE >= 600 and 'player_from_shop3.png' not in purchased_ships:
                        purchased_ships.append('player_from_shop3.png')
                        btn_sound.play()
                        player_stats[:-1] = ship4_characteristics[:-1]
                        player_stats[-1] = 'player_from_shop3.png'
                        SCORE -= ship4_characteristics[-1]
                        cur.execute("""UPDATE score SET SCORE = ?""", (SCORE,))
                        cur.execute("""INSERT INTO purchased_ships(image) VALUES(?)""", (player_stats[-1],))
                        con.commit()
                        return

        if select_btn.is_clicked():
            for rect in rects:
                if rect.active:
                    if rect.id == 0:
                        btn_sound.play()
                        player_stats[:-1] = ship1_characteristics[:-1]
                        player_stats[-1] = 'player.png'
                        return
                    if rect.id == 1 and 'player_from_shop1.png' in purchased_ships:
                        btn_sound.play()
                        player_stats[:-1] = ship2_characteristics[:-1]
                        player_stats[-1] = 'player_from_shop1.png'
                        return
                    if rect.id == 2 and 'player_from_shop2.png' in purchased_ships:
                        btn_sound.play()
                        player_stats[:-1] = ship3_characteristics[:-1]
                        player_stats[-1] = 'player_from_shop2.png'
                        return
                    if rect.id == 3 and 'player_from_shop3.png' in purchased_ships:
                        btn_sound.play()
                        player_stats[:-1] = ship4_characteristics[:-1]
                        player_stats[-1] = 'player_from_shop3.png'
                        return

        for rect in rects:
            rect.update()
            rect.draw(shop_surface)

        buy_btn.render(SCREEN)
        select_btn.render(SCREEN)

        buy_btn.play_sound_if_btn_selected()
        select_btn.play_sound_if_btn_selected()

        clock.tick(FPS)
        pygame.display.flip()


def game_over():
    global dx, dy, k_up_clicked, k_right_clicked, k_down_clicked, k_left_clicked

    game_over_surface = pygame.Surface(SIZE)
    game_over_img = pygame.transform.scale(load_image('game_over.png', -1), (300, 200))
    game_over_surface.set_alpha(30)

    font = pygame.font.SysFont('Jokerman', 40)
    clock = pygame.time.Clock()

    retry_btn = ClassicButton(font, 340, 300, 'Retry')
    back_to_menu_btn = ClassicButton(font, 300, 360, 'Back to menu')
    is_running = True

    game_over_sound.play()

    while is_running:
        SCREEN.blit(game_over_surface, (0, 0))
        SCREEN.blit(game_over_img, (250, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        if retry_btn.is_clicked():
            k_up_clicked = False
            k_right_clicked = False
            k_down_clicked = False
            k_left_clicked = False
            dx, dy = 0, 0
            game_over_sound.stop()
            btn_sound.play()
            delete_all_sprites()
            main()

        if back_to_menu_btn.is_clicked():
            dx, dy = 0, 0
            game_over_sound.stop()
            btn_sound.play()
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
    for heart in hearts_group:
        heart.kill()
