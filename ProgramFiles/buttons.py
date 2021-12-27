from ProgramFiles.consts import pygame

pygame.mixer.init()
btn_sound = pygame.mixer.Sound('music\\button.wav')


class Button:
    def __init__(self, x, y, text_of_article, color_of_article=(255, 0, 0), color_of_selected_article=(0, 255, 0)):
        self.x, self.y = x, y
        self.text_of_article = text_of_article
        self.color_of_article = color_of_article
        self.color_of_selected_article = color_of_selected_article

    def render(self, surface, font, func=None):
        mouse_pos = pygame.mouse.get_pos()
        mouse_btn_clicked = pygame.mouse.get_pressed()

        if self.x < mouse_pos[0] < self.x + 200 and self.y < mouse_pos[1] < self.y + 50:
            surface.blit(font.render(self.text_of_article, 1, self.color_of_article), (self.x, self.y))
            if mouse_btn_clicked[0] == 1:
                btn_sound.play()
                pygame.time.delay(200)
                if func is not None:
                    func()
        else:
            surface.blit(font.render(self.text_of_article, 1, self.color_of_selected_article), (self.x, self.y))

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_btn_clicked = pygame.mouse.get_pressed()
        if self.x < mouse_pos[0] < self.x + 200 and self.y < mouse_pos[1] < self.y + 50 and mouse_btn_clicked[0] == 1:
            return True
