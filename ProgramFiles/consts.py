import pygame
import sqlite3

# !!! CONSTS !!!
GAME_TITLE = "SPACE WARS"
SIZE = WIDTH, HEIGHT = 800, 800
BACKGROUND_COLOR = pygame.Color('black')
FPS = 60
con = sqlite3.connect('settings.db')
COMPLEXITY = list(*con.cursor().execute("""SELECT difficult FROM difficultness"""))[0]
