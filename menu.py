"""
This file contains the menu UI. Just like Game it borrows a window object.
"""

import pygame

from game import Game
from settings import Settings
import fonts
from config import config
from ui_elements import Button


class Menu:
    def __init__(self, window):
        """
        Initialize a menu object.
        :param window: The window.Window the class borrows.
        """

        # Claim the window and initialize the clock
        self.window = window
        self.window.set_caption("Game of Life")
        self.window.set_icon(pygame.image.load("resources/icon.png"))
        self.clock = pygame.time.Clock()

        self.cw = None
        self.ch = None

        # Create the grid surface used in rendering the menu
        self.create_grid()

        self.buttons = []

        self.buttons.append(Button(
            "Play",
            fonts.main,
            config.color_buttons,
            self.play,
            (self.window.width // 2, self.window.height // 2 - 140, 300, 120),
            "cc",
            text_color=config.color_buttons_text,
            border_color=config.color_buttons_border
        ))

        self.buttons.append(Button(
            "Settings",
            fonts.main,
            config.color_buttons,
            self.settings,
            (self.window.width // 2, self.window.height // 2, 300, 120),
            "cc",
            text_color=config.color_buttons_text,
            border_color=config.color_buttons_border
        ))

        self.buttons.append(Button(
            "Exit",
            fonts.main,
            config.color_buttons,
            self.exit,
            (self.window.width // 2, self.window.height // 2 + 140, 300, 120),
            "cc",
            text_color=config.color_buttons_text,
            border_color=config.color_buttons_border
        ))

        self.running = False

    # noinspection PyAttributeOutsideInit
    def create_grid(self):
        """
        This function draws the grid that will be used to split the cells visually.
        It uses the Surface.convert_alpha and pygame.SRCALPHA to create the transparent squares.
        :return: None
        """

        # Define the cell width and height
        self.cw = self.window.width // config.w
        self.ch = self.window.height // config.h

        self.grid = pygame.Surface((self.window.width, self.window.height), pygame.SRCALPHA)
        self.grid.fill(config.color_cell_dead)

        for i in range(config.h):
            for j in range(config.w):
                rect = (self.cw * j, self.ch * i, self.cw, self.ch)
                pygame.draw.rect(self.grid, config.color_grid, rect, 2)

        self.grid = self.grid.convert_alpha()

    def render(self):
        """
        Render the menu.
        Is only really called when starting the menu, and returning from the game, as it is static.
        :return: None
        """

        # Draw the grid on the screen
        self.window.blit(self.grid, (0, 0))

        for button in self.buttons:
            button.render(self.window.window)

        # Update the entire scene, as this is a close to one-time call
        self.window.update()

    def settings(self):
        """
        The callback function for the "settings" button
        :return: None
        """

        # Initialize, run and delete the settings object
        settings = Settings(self.window)
        settings.run()
        del settings

        # Render the scene once again, to overwrite the settings rendering
        self.create_grid()
        self.render()

    def play(self):
        """
        The callback function for the "play" button.
        :return: None
        """

        # Initialize, run and delete the game object
        game = Game(self.window)
        game.run()
        del game

        # Render the scene once again, to overwrite the games rendering
        self.render()

    def exit(self):
        """
        Exit the menu to desktop.

        :return: None
        """

        self.running = False

    def run(self):
        """
        Run the menu itself.
        :return: None
        """

        # Render the menu once at the start
        self.render()
        self.running = True

        while self.running:
            # Get the events that pygame has collected
            for event in pygame.event.get():
                # If the user has pressed escape, exit to the previous level
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.exit()

                # If the user has pressed mouse-button up
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        # Get the position of the cursor
                        x, y = pygame.mouse.get_pos()

                        # Iterate through buttons, and check for collision
                        for button in self.buttons:
                            if button.collidepoint(x, y):
                                button.callback()

            self.clock.tick(24)
