"""
This file contains the menu UI. Just like Game it borrows a window object.
"""

import pygame
import json

from game import Game
import fonts
from ui_elements import Button


class Menu:
    def __init__(self, window):
        """
        Initialize a menu object.
        :param window: The window.Window the class borrows.
        """

        # Claim the window and initialize the clock
        self.window = window
        self.clock = pygame.time.Clock()

        # Load the config
        self.load_config()

        # Create the grid surface used in rendering the menu
        self.create_grid()

        # Initialize the custom button, derived from a pygame.Rect
        self.button = Button(
            "Play",
            fonts.main,
            self.color_buttons,
            self.play,
            (self.window.width // 2, self.window.height // 2, 300, 120),
            True,
            text_color=self.color_text,
            border_color=self.color_buttons_border
        )

    # noinspection PyAttributeOutsideInit
    def load_config(self):
        """
        Load the config from config.json.
        Only assigns some of the variables, as it doesn't need to save them again.
        :return: None
        """

        with open("config.json", "r") as f:
            data = json.load(f)

        # Get the dimensions of the grid
        self.w = data["field-dimensions"]["w"]
        self.h = data["field-dimensions"]["h"]

        # Calculate the cell width and height from the window dimensions
        self.cw = self.window.width // self.w
        self.ch = self.window.height // self.h

        # Assign all the colors
        self.color_bg = data["colors"]["color-bg"]
        self.color_cell_alive = data["colors"]["color-cell-alive"]
        self.color_cell_dead = data["colors"]["color-cell-dead"]
        self.color_grid = data["colors"]["color-grid"]
        self.color_buttons = data["colors"]["color-buttons"]
        self.color_buttons_border = data["colors"]["color-buttons-border"]
        self.color_text = data["colors"]["color-text"]

    # noinspection PyAttributeOutsideInit
    def create_grid(self):
        """
        This function draws the grid that will be used to split the cells visually.
        It uses the Surface.convert_alpha and pygame.SRCALPHA to create the transparent squares.
        :return: None
        """
        self.grid = pygame.Surface((self.window.width, self.window.height), pygame.SRCALPHA)
        self.grid.fill(self.color_cell_dead)

        for i in range(self.h):
            for j in range(self.w):
                rect = (self.cw * j, self.ch * i, self.cw, self.ch)
                pygame.draw.rect(self.grid, self.color_grid, rect, 2)

        self.grid = self.grid.convert_alpha()

    def render(self):
        """
        Render the menu.
        Is only really called when starting the menu, and returning from the game, as it is static.
        :return: None
        """

        # Draw the grid on the screen
        self.window.blit(self.grid, (0, 0))

        self.button.render(self.window.window)

        # Update the entire scene, as this is a close to one-time call
        self.window.update()

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

    def run(self):
        """
        Run the menu itself.
        :return: None
        """

        # Render the menu once at the start
        self.render()
        running = True

        while running:
            # Get the events that pygame has collected
            for event in pygame.event.get():
                # If the user has pressed escape, exit to the previous level
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                # If the user has pressed mouse-button up
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        # Get the position of the cursor
                        x, y = pygame.mouse.get_pos()

                        # Check if the cursor collides with the button
                        if self.button.collidepoint(x, y):
                            # Call the buttons callback
                            # I would like to have the callbacks handled differently, but couldn't come up with anything
                            self.button.callback()

            self.clock.tick(60)
