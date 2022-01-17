from ProgramFiles.consts import pygame
from ProgramFiles.base_classes import Button, BoxAndRect


# кнопки меню
class ClassicButton(Button):
    def __init__(self, font, x, y, text_of_article, color_of_article=(0, 255, 0), color_of_selected_article=(255, 0, 0)):
        super().__init__(x, y)
        self.text_of_article = text_of_article
        self.font = font
        self.off_string = font.render(self.text_of_article, 1, color_of_article)
        self.on_string = font.render(self.text_of_article, 1, color_of_selected_article)
        self.selected = True

    def render(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.off_string.get_width()\
                and self.y < mouse_pos[1] < self.y + self.off_string.get_height():
            surface.blit(self.on_string, (self.x, self.y))
        else:
            surface.blit(self.off_string, (self.x, self.y))

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_btn_clicked = pygame.mouse.get_pressed()

        if self.x < mouse_pos[0] < self.x + self.off_string.get_width() \
                and self.y < mouse_pos[1] < self.y + self.off_string.get_height() and mouse_btn_clicked[0] == 1:
            return True


# кнопки в настройках
class SpinBox(Button):
    def __init__(self, x, y, loud_of_sound):
        super().__init__(x, y)
        self.max_value = 0.9
        self.min_value = 0.1
        self.step = 0.1
        self.curr_value = loud_of_sound
        self.triangle_points = [((self.x - 10, self.y + 40), (self.x - 30, self.y + 20), (self.x - 10, self.y)),
                                ((self.x + 360, self.y + 40), (self.x + 360, self.y), (self.x + 380, self.y + 20))]
        self.rect1 = pygame.Rect(self.x - 35, self.y - 5, 35, 50)
        self.rect2 = pygame.Rect(self.x + 350, self.y - 5, 35, 50)

    def render(self, surface):
        font = pygame.font.Font(None, 38)
        mouse_pos = pygame.mouse.get_pos()
        mouse_btn_clicked = pygame.mouse.get_pressed()
        pygame.draw.rect(surface, (160, 160, 160), (self.x + 10, self.y, 330, 35))

        self.increase_rect(surface)
        self.decrease_rect(surface)
        pygame.draw.polygon(surface, (pygame.Color('white')), self.triangle_points[0])
        pygame.draw.polygon(surface, (pygame.Color('white')), self.triangle_points[1])

        if self.rect1.collidepoint(mouse_pos) and mouse_btn_clicked[0] == 1:
            # задержка времени чтобы значения не перематывались быстро(типа фпс)
            pygame.time.delay(200)
            self.decrease()
        elif self.rect2.collidepoint(mouse_pos) and mouse_btn_clicked[0] == 1:
            pygame.time.delay(200)
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


class InputBox(BoxAndRect, Button):
    def __init__(self, x, y, w, h, text, active_color=(255, 0, 0), inactive_color=(0, 255, 0)):
        super().__init__(x, y, w, h, active_color, inactive_color)
        self.text = text.capitalize()
        self.font = pygame.font.Font(None, h + 10)
        self.text_has_changed = False
        self.active = False
        self.curr_color = None
        self.selected = True

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_btn_clicked = pygame.mouse.get_pressed()
        if mouse_btn_clicked[0] == 1:
            if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
                self.active = True
            else:
                self.active = False
            self.curr_color = self.active_color if self.active else self.inactive_color

    def draw(self, surface, border_radius=5):
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            pygame.draw.rect(surface, self.active_color,
                             (self.x, self.y, self.width, self.height), border_radius=border_radius)
            surface.blit(self.font.render(self.text, 1, (255, 255, 255)), (self.x + 5, self.y))
        else:
            pygame.draw.rect(surface, self.curr_color,
                             (self.x, self.y, self.width, self.height), border_radius=border_radius)
            surface.blit(self.font.render(self.text, 1, (255, 255, 255)), (self.x + 5, self.y))

    def update_text(self, event):
        name_of_key = pygame.key.name(event.key)
        if self.curr_color == self.active_color:
            self.text = name_of_key.capitalize()
            self.text_has_changed = True
        else:
            self.text_has_changed = False

    def text_changed(self):
        return self.text_has_changed

    def is_selected(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            return True
        return False


class AnimatedRect(BoxAndRect):
    def __init__(self, x, y, w, h, id, active_color=(255, 0, 0), inactive_color=(0, 255, 0)):
        super().__init__(x, y, w, h, active_color, inactive_color)
        self.active = False
        self.curr_color = inactive_color
        self.id = id

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_btn_clicked = pygame.mouse.get_pressed()
        if mouse_btn_clicked[0] == 1:
            if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
                self.active = True
            else:
                self.active = False
            self.curr_color = self.active_color if self.active else self.inactive_color

    def draw(self, surface, width=3):
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            pygame.draw.rect(surface, self.active_color, (self.x, self.y, self.width, self.height), width=width)
        else:
            pygame.draw.rect(surface, self.curr_color, (self.x, self.y, self.width, self.height), width=width)


class ShopButton(Button):
    def __init__(self, x, y, w, h, text='Buy', color_of_article=(0, 255, 0), color_of_selected_article=(255, 0, 0)):
        super().__init__(x, y, color_of_article, color_of_selected_article)
        self.width, self.height = w, h
        self.text = text

    def render(self, surface):
        font = pygame.font.SysFont('Jokerman', 48)
        mouse_pos = pygame.mouse.get_pos()

        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + 70:
            pygame.draw.rect(surface, self.color_of_selected_article, (self.x, self.y, self.width, 70), border_radius=10)
        else:
            pygame.draw.rect(surface, self.color_of_article, (self.x, self.y, self.width, 70), border_radius=10)
        surface.blit(font.render(self.text, 1, (255, 255, 255)), (self.x + 50, self.y - 10))

    def is_selected(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + 70:
            return True
        return False
