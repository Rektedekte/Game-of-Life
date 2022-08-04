"""
This file acts as a container for all the fonts used in the game.
It can be viewed like an oop container class, just without the class.
"""

import pygame
from screeninfo import get_monitors

# Scale fonts to the monitor size, to ensure continuity
monitor = get_monitors()[0]

# Initialize the font module
pygame.font.init()

# This is the main font to be used in ui elements
main = pygame.font.Font(None, int(50 * min(monitor.width / 1920, monitor.height / 1080)))
