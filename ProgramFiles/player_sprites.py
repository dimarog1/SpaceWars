from ProgramFiles.base_classes import *


# Игрок
class Player(Ship, pygame.sprite.Sprite):
    def __init__(self, screen, position=(0, 0)):
        Ship.__init__(self, screen, position)
        pygame.sprite.Sprite.__init__(self, player_group)
        self.image = pygame.transform.scale(load_image('player.png'), (100, 100))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(WIDTH // 2 - self.width // 2, HEIGHT + 10)

    def starting_ship(self):
        if self.rect.y >= HEIGHT - 130:
            return True
        return False


# Выстрел игрока
class PlayerProjectileLevelOne(Projectile, pygame.sprite.Sprite):
    def __init__(self, parent_ship):
        Projectile.__init__(self, parent_ship)
        pygame.sprite.Sprite.__init__(self, player_shots_group)
        self.image = pygame.transform.scale(load_image('shot.png'), (17, 27))

    def update(self):
        # Столкновения с кораблём
        for enemy in enemy_group:
            if pygame.sprite.collide_mask(self, enemy):
                enemy.activate_hp_bar()
                enemy.hp -= 1
                self.kill()
                return

        # Перемщение снаряда
        if self.rect.y - self.speed_of_shot >= 0 - self.height:
            self.rect.y -= self.speed_of_shot
        else:
            self.kill()
