from ProgramFiles.consts import pygame

pygame.mixer.init()

boom_sound = pygame.mixer.Sound('music\\boom.wav')
shoot_sound = pygame.mixer.Sound(r'.\music\shoot.wav')
btn_sound = pygame.mixer.Sound('music\\button.wav')
fon_sound = pygame.mixer.Sound('music\\fon_music.mp3')
selected_btn_sound = pygame.mixer.Sound('music\\selected_sound.wav')
game_over_sound = pygame.mixer.Sound('music\\game_over1.wav')
gained_bonus_sound = pygame.mixer.Sound('music\\gain_bonus.wav')
boss_second_attack_sound = pygame.mixer.Sound('music\\boss_second_attack.wav')
level_completed_sound = pygame.mixer.Sound('music\\completed.wav')
