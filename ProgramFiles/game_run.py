from ProgramFiles.consts import *
from ProgramFiles.units_sprites import *
from Buttons import Button
from itertools import cycle


def terminate():
    pygame.quit()
    exit(0)


pygame.init()
pygame.mixer.init()
SCREEN = pygame.display.set_mode(SIZE)
shoot_sound = pygame.mixer.Sound('data\\shoot.wav')
shoot_sound.set_volume(0.3)


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


GAME_TITLE_IMG = pygame.transform.scale(load_image('game_title.png', -1), (300, 200))


def menu():
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.mixer.init()

    font = pygame.font.SysFont('Jokerman', 48)
    fon_sound = pygame.mixer.Sound('data\\fon_music.mp3')
    clock = pygame.time.Clock()

    first_bg = FirstBg()
    second_bg = SecondBg()

    running = True

    play_btn = Button(350, 240, 'Play')
    shop_btn = Button(350, 300, 'Shop')
    settings_btn = Button(350, 360, 'Settings')
    quit_btn = Button(350, 420, 'Quit')

    fon_sound.set_volume(0.5)
    fon_sound.play(-1)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()

        if play_btn.is_clicked():
            fon_sound.stop()

        bg_group.draw(SCREEN)
        bg_group.update()
        SCREEN.blit(GAME_TITLE_IMG, (250, 50))

        play_btn.render(SCREEN, font, func=main)
        shop_btn.render(SCREEN, font)
        settings_btn.render(SCREEN, font)
        quit_btn.render(SCREEN, font, func=terminate)

        clock.tick(FPS)
        pygame.display.flip()


def start_screen():
    pygame.display.set_caption(GAME_TITLE)

    clock = pygame.time.Clock()
    blink_event = pygame.USEREVENT + 0

    first_bg = FirstBg()
    second_bg = SecondBg()

    font = pygame.font.Font(None, 48)
    string_rendered = font.render("Press space key to start", True, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.center = SCREEN.get_rect().center
    intro_rect.top, intro_rect.x = 700, 200
    off_intro_text = pygame.Surface(intro_rect.size)
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


def main():
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()

    running = True

    player = Player()
    enemy = EnemyLevelOne()
    dx = dy = 0
    count = 1

    first_bg = FirstBg()
    second_bg = SecondBg()

    while running:

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

        if count % 15 == 0:
            # ВВылет выстрела
            shot = ProjectileLevelOne(player)
            shoot_sound.play()

        bg_group.draw(SCREEN)
        bg_group.update()
        player_shots_group.update()
        player.change_pos(dx, dy)

        clock.tick(FPS)

        # Отрисовка
        player_group.draw(SCREEN)
        enemy_group.draw(SCREEN)
        player_shots_group.draw(SCREEN)
        pygame.display.flip()
        count += 1

    pygame.mixer.quit()
    terminate()
