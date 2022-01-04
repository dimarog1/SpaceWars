import json

import pygame
import sqlite3

from ProgramFiles.consts import *
from ProgramFiles.enemy_sprites import *
from ProgramFiles.player_sprites import *
from ProgramFiles.buttons import Button, SpinBox
from itertools import cycle
from music.sounds import boom_sound, shoot_sound, btn_sound, fon_sound


def terminate():
    pygame.quit()
    exit(0)


pygame.init()
pygame.mixer.init()
SCREEN = pygame.display.set_mode(SIZE)

con = sqlite3.connect('settings.db')
cur = con.cursor()
res = list(cur.execute("""SELECT music_sound, music_effects_sound FROM settings_values"""))


loud_of_menu_music, loud_of_effects = list(map(float, *res))

first_bg = FirstBg()
second_bg = SecondBg()

GAME_TITLE_IMG = pygame.transform.scale(load_image('game_title.png', -1), (300, 200))


shoot_sound.set_volume(loud_of_effects)
boom_sound.set_volume(loud_of_effects)
fon_sound.set_volume(loud_of_menu_music)
btn_sound.set_volume(loud_of_menu_music)


def menu():
    pygame.mixer.init()
    font = pygame.font.SysFont('Jokerman', 48)
    clock = pygame.time.Clock()

    running = True

    music_sound_spinbox = SpinBox(400, 10, loud_of_menu_music)
    music_effects_sound_spinbox = SpinBox(400, 70, loud_of_effects)

    play_btn = Button(350, 240, 'Play')
    shop_btn = Button(350, 300, 'Shop')
    settings_btn = Button(350, 360, 'Settings')
    quit_btn = Button(350, 420, 'Quit')

    fon_sound.play(-1)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()

        if play_btn.is_clicked():
            fon_sound.stop()
            btn_sound.play()
            main()

        if quit_btn.is_clicked():
            btn_sound.play()
            pygame.time.delay(200)
            terminate()

        if settings_btn.is_clicked():
            btn_sound.play()
            settings(music_sound_spinbox, music_effects_sound_spinbox)

        bg_group.draw(SCREEN)
        bg_group.update()
        SCREEN.blit(GAME_TITLE_IMG, (250, 50))

        play_btn.render(SCREEN, font)
        shop_btn.render(SCREEN, font)
        settings_btn.render(SCREEN, font)
        quit_btn.render(SCREEN, font)

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
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if intro_rect.x < event.pos[0] < intro_rect.x + intro_rect.width\
                        and intro_rect.y < event.pos[1] < intro_rect.height + intro_rect.y:
                    menu()
                    return
            elif event.type == blink_event:
                blink_surface = next(blink_surfaces)

        bg_group.draw(SCREEN)
        bg_group.update()

        SCREEN.blit(GAME_TITLE_IMG, (250, 50))
        SCREEN.blit(blink_surface, intro_rect)

        clock.tick(FPS)
        pygame.display.flip()


def settings(menu_music, effects_music):
    clock = pygame.time.Clock()
    surface = pygame.Surface((WIDTH, HEIGHT))
    font = pygame.font.Font(None, 38)

    surface.fill((128, 128, 128))
    surface.set_alpha(30)

    back_btn = Button(20, 750, 'Back')
    apply_btn = Button(700, 750, 'Apply')

    surface.blit(font.render('Menu music', 1, (255, 255, 255)), (20, 20))
    surface.blit(font.render('Effects music', 1, (255, 255, 255)), (20, 80))

    is_running = True
    while is_running:
        SCREEN.blit(surface, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                terminate()
        if back_btn.is_clicked():
            return
        elif apply_btn.is_clicked():
            cur.execute("""UPDATE settings_values
                                SET music_sound = ?""", (str(menu_music.curr_value),))
            con.commit()
            cur.execute("""UPDATE settings_values
                                SET music_effects_sound = ?""", (str(effects_music.curr_value),))
            con.commit()

            shoot_sound.set_volume(effects_music.curr_value)
            boom_sound.set_volume(effects_music.curr_value)
            fon_sound.set_volume(menu_music.curr_value)
            btn_sound.set_volume(menu_music.curr_value)

        menu_music.render(surface, font)
        effects_music.render(surface, font)

        back_btn.render(surface, font)
        apply_btn.render(surface, font)

        clock.tick(FPS)
        pygame.display.flip()


def start_enemy_wave(wave):
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
        y = 50
        print(x, y)
        enemy.set_start_pos(x, y)
        print(enemy)
        print('---')
        enemies.add(enemy)
        k += 1
    return enemies


def main():
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()

    # Загрузка уровня
    waves = list()
    with open(r'.\levels\level_one.json') as level:
        level = json.loads(level.read())
    for wave in level:
        waves.append(level[wave])

    player = Player()
    # enemy1 = EnemyLevelFour((100, 50))
    dx = dy = 0
    count = 1

    # Скорость выстрела (чем меньше число, тем больше скорость)
    player_speed_shooting = 15
    enemy_speed_shooting = 90

    # Выпуск корабля игрока
    while player.starting_ship():
        player.rect.y -= 1

        bg_group.draw(SCREEN)
        bg_group.update()
        clock.tick(FPS)

        # Отрисовка
        player_group.draw(SCREEN)
        enemy_group.draw(SCREEN)
        pygame.display.flip()

    print(waves)
    enemies_of_wave = start_enemy_wave(waves[0])
    del waves[0]
    for e in enemies_of_wave:
        print(e)

    running = True

    while running:

        if len(enemies_of_wave) == 0:
            if len(waves) != 0:
                enemies_of_wave = start_enemy_wave(waves[0])
                del waves[0]
            else:
                running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    dy += -1
                if event.key == pygame.K_DOWN:
                    dy += 1
                if event.key == pygame.K_LEFT:
                    dx += -1
                if event.key == pygame.K_RIGHT:
                    dx += 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    dy += 1
                if event.key == pygame.K_DOWN:
                    dy += -1
                if event.key == pygame.K_LEFT:
                    dx += 1
                if event.key == pygame.K_RIGHT:
                    dx += -1

        if count % player_speed_shooting == 0:
            # Вылет выстрела
            if player.alive():
                player_shot = PlayerProjectileLevelOne(player)
                shoot_sound.play()

        if count % enemy_speed_shooting == 0:
            for enemy in enemy_group:
                if enemy.alive():
                    enemy_shot = EnemyProjectile(enemy)
                    shoot_sound.play()

        bg_group.draw(SCREEN)
        bg_group.update()

        # Удаление кораблей, если они уничтожены
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
        enemy_group.draw(SCREEN)
        enemies_of_wave.draw(SCREEN)
        player_shots_group.draw(SCREEN)
        enemy_shots_group.draw(SCREEN)
        boom_group.draw(SCREEN)
        pygame.display.flip()
        count += 1

    pygame.mixer.quit()
    con.close()
    terminate()
