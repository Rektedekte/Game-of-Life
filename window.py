"""
This is a small file containing a class that simplifies creating and interacting with a pygame window.
"""

import pygame
from screeninfo import get_monitors
from typing import Tuple


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

    def scale_x(self, x: int) -> int:
        """
        Scale x coordinates relative to display width.

        :param x: x coordinate to scale
        :return: Scaled x coordinate
        """

        return int(x * (self.monitor.width / 1920))

    def scale_y(self, y: int) -> int:
        """
        Scale y coordinates relative to display height.

        :param y: y coordinate to scale
        :return: Scaled y coordinate
        """

        return int(y * (self.monitor.height / 1080))

    def scale_xy(self, x: int, y: int) -> Tuple[int, int]:
        """
        Scale x and y coordinates relative to display size.

        :param x: x coordinate to scale
        :param y: y coordinate to scale
        :return: Scale coordinates
        """

        return self.scale_x(x), self.scale_y(y)

    def scale_rect(self, rect: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
        """
        Scale rect coordinates relative to display size.

        :param rect: rect to scale
        :return: The scaled rect
        """

        return self.scale_x(rect[0]), self.scale_y(rect[1]), self.scale_x(rect[2]), self.scale_y(rect[3])

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
