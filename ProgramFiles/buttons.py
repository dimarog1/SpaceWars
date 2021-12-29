from ProgramFiles.consts import pygame


# кнопки меню
class Button:
    def __init__(self, x, y, text_of_article, color_of_article=(255, 0, 0), color_of_selected_article=(0, 255, 0)):
        self.x, self.y = x, y
        self.text_of_article = text_of_article
        self.color_of_article = color_of_article
        self.color_of_selected_article = color_of_selected_article

    def render(self, surface, font):
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + 200 and self.y < mouse_pos[1] < self.y + 50:
            surface.blit(font.render(self.text_of_article, 1, self.color_of_article), (self.x, self.y))
        else:
            surface.blit(font.render(self.text_of_article, 1, self.color_of_selected_article), (self.x, self.y))

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_btn_clicked = pygame.mouse.get_pressed()
        if self.x < mouse_pos[0] < self.x + 200 and self.y < mouse_pos[1] < self.y + 50 and mouse_btn_clicked[0] == 1:
            return True


# кнопки в настройках
class SpinBox:
    def __init__(self, x, y, loud_of_sound):
        self.x, self.y = x, y
        self.max_value = 0.9
        self.min_value = 0.1
        self.step = 0.1
        self.curr_value = loud_of_sound
        self.triangle_points = [((self.x - 10, self.y + 40), (self.x - 30, self.y + 20), (self.x - 10, self.y)),
                                ((self.x + 360, self.y + 40), (self.x + 360, self.y), (self.x + 380, self.y + 20))]
        self.rect1 = pygame.Rect(self.x - 35, self.y - 5, 35, 50)
        self.rect2 = pygame.Rect(self.x + 350, self.y - 5, 35, 50)

    def render(self, surface, font):
        mouse_pos = pygame.mouse.get_pos()
        mouse_btn_clicked = pygame.mouse.get_pressed()
        pygame.draw.rect(surface, (160, 160, 160), (self.x + 10, self.y, 330, 35))

        self.increase_rect(surface)
        self.decrease_rect(surface)
        pygame.draw.polygon(surface, (pygame.Color('white')), self.triangle_points[0])
        pygame.draw.polygon(surface, (pygame.Color('white')), self.triangle_points[1])
        if self.rect1.collidepoint(mouse_pos) and mouse_btn_clicked[0] == 1:
            # задержка времени чтобы значения не перематывались быстро(типа фпс)
            pygame.time.delay(120)
            self.decrease()
        elif self.rect2.collidepoint(mouse_pos) and mouse_btn_clicked[0] == 1:
            pygame.time.delay(120)
            self.increase()
        surface.blit(font.render(str(round(self.curr_value, 1)), 1, pygame.Color('black')), (self.x + 10, self.y + 5))

    def increase_rect(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect1.x < mouse_pos[0] < self.rect1.x + self.rect1.w\
                and self.rect1.y < mouse_pos[1] < self.rect1.y + self.rect1.h:
            pygame.draw.rect(surface, (187, 187, 187), (self.rect1.x, self.rect1.y, self.rect1.w, self.rect1.h))
        else:
            pygame.draw.rect(surface, (128, 128, 128), (self.rect1.x, self.rect1.y, self.rect1.w, self.rect1.h))

    def decrease_rect(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect2.x < mouse_pos[0] < self.rect2.x + self.rect2.w\
                and self.rect2.y < mouse_pos[1] < self.rect2.y + self.rect2.h:
            pygame.draw.rect(surface, (187, 187, 187), (self.rect2.x, self.rect2.y, self.rect2.w, self.rect2.h))
        else:
            pygame.draw.rect(surface, (128, 128, 128), (self.rect2.x, self.rect2.y, self.rect2.w, self.rect2.h))

    def increase(self):
        if self.curr_value <= self.max_value:
            self.curr_value += self.step

    def decrease(self):
        if self.curr_value >= self.min_value:
            self.curr_value -= self.step
