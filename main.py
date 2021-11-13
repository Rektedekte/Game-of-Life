"""
The main script that creates the window and starts the game.
Any modifications to the script-path should be done here.
"""

from menu import Menu
from window import Window
import pygame

if __name__ == "__main__":
    pygame.font.init()

    window = Window()
    menu = Menu(window)
    menu.run()
    window.close()
