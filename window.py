"""
This is a small file containing a class that simplifies creating and interacting with a pygame window.
"""

import pygame
from screeninfo import get_monitors


class Window:
    def __init__(self, width: int = None, height: int = None, fullscreen: bool = True):
        """
        Initialize the window used to abstract the pygame.Surface class.
        :param width: An int representing the width to resize to
        :param height: An int representing the height to resize to
        :param fullscreen: A bool representing the windows fullscreen state
        """

        # Initialise if not already initialized
        if not pygame.get_init():
            pygame.init()

        # Get the monitor
        self.monitor = get_monitors()[0]

        self.width = None
        self.height = None
        self.window = None

        # Call the function to initialize a window
        self.resize(width, height, fullscreen)

        # Rewrite som functions into this context to simplify working with this class
        self.blit = self.window.blit
        self.fill = self.window.fill

    # Assign som pygame functions as part of this class
    close = pygame.quit
    update = pygame.display.update
    draw = pygame.draw
    set_caption = pygame.display.set_caption
    set_icon = pygame.display.set_icon

    def resize(self, width: int = None, height: int = None, fullscreen: bool = True):
        """
        This function serves as an abstraction for simply initialising a new window,
        and makes the transition from one UI controller to another more logical.

        :param width: An int representing the width to resize to
        :param height: An int representing the height to resize to
        :param fullscreen: A bool representing the windows fullscreen state
        :return: None
        """

        # Get the dimensions of said monitor, if not otherwise specified
        self.width = width
        self.height = height

        if not isinstance(self.width, int):
            self.width = self.monitor.width
        if not isinstance(self.height, int):
            self.height = self.monitor.height

        # Create the pygame window
        if fullscreen:
            self.window = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((self.width, self.height))
