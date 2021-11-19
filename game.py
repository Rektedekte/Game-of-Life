"""
This file contains just the game class, that can be instantiated with a window object.
All code related to the game of life is contained here.
"""

import pygame
import numpy as np
from config import config


class Game:
    def __init__(self, window):
        """
        Initialise the game, borrowing an existent pygame window, of the window.Window type.
        :param window: pygame window, of type window.Window
        """

        # Adopt the window given to it, ensuring compatibility from different sources
        self.window = window
        self.clock = pygame.time.Clock()

        # Initialize the local animation variables
        self.animate_clock = pygame.time.Clock()
        self.animate_switch = False

        # Calculate the cell width and height for rendering
        self.cw = self.window.width // config.w
        self.ch = self.window.height // config.h

        # Create the map from the config variables, and load the neigh_map
        self.map: np.ndarray = np.zeros((config.h, config.w), dtype="bool")
        self.neigh_map: list = [[self.get_neighbors(i, j) for j in range(config.w)] for i in range(config.h)]

        # Create the grid used to split the cells visually
        self.create_grid()

        # A variable that stores information about what to render, used by the render function
        self.draw_new = {
            "all": True,  # Flag to draw everything, is initially on for first render
            "cells": []  # A list of cells to update
        }

    def get_neighbors(self, i: int, j: int) -> np.ndarray:
        """
        Get the neighbors of a particular cell, taking the borders into account.
        :param i: Columns, the first index of the grid
        :param j: Rows, the second index of the grid
        :return: A np.ndarray of max 3x3, tied to self.map
        """

        return self.map[max(0, i - 1): min(config.h - 1, i + 2), max(0, j - 1): min(config.w - 1, j + 2)]

    def refresh_neighbors(self):
        """
        Refresh the neighbor map, is used to quickly calculate the sum of neighbors.
        :return: None
        """

        self.neigh_map: list = [[self.get_neighbors(i, j) for j in range(config.w)] for i in range(config.h)]

    def get_neighbors_sum(self, i: int, j: int) -> int:
        """
        Get the sum of all neighbors, including the cell itself.
        :param i: Columns, the first index of the grid
        :param j: Rows, the second index of the grid
        :return: The integer sum of all neighbors
        """

        return int(np.sum(self.neigh_map[i][j]))

    def game_tick(self):
        """
        Calculate the next tick in the game.
        This means creating a new board, and filling all cells based on the rules of the game of life.
        :return: None
        """
        new_board = np.zeros((config.h, config.w), dtype="bool")

        for i in range(config.h):
            for j in range(config.w):
                if self.map[i, j]:  # Cell is alive
                    if not 2 < self.get_neighbors_sum(i, j) < 5:  # Cell dies by over-/underpopulation
                        new_board[i, j] = 0
                        self.draw_new["cells"].append((i, j))
                    else:
                        new_board[i, j] = 1

                else:  # Cell is dead
                    if self.get_neighbors_sum(i, j) == 3:  # Cell lives by reproduction
                        new_board[i, j] = 1
                        self.draw_new["cells"].append((i, j))
                    else:
                        new_board[i, j] = 0

        # Overwrite the current map
        self.map = new_board
        # Refresh the neigh_map, which is immutably tied to the board
        self.refresh_neighbors()

    # noinspection PyAttributeOutsideInit
    def create_grid(self):
        """
        This function draws the grid that will be used to split the cells visually.
        It uses the Surface.convert_alpha and pygame.SRCALPHA to create the transparent squares.
        :return: None
        """
        self.grid = pygame.Surface((self.window.width, self.window.height), pygame.SRCALPHA)

        for i, j in np.ndindex(self.map.shape):
            rect = (self.cw * j, self.ch * i, self.cw, self.ch)
            pygame.draw.rect(self.grid, config.color_grid, rect, 2)

        self.grid = self.grid.convert_alpha()

    def render(self):
        """
        The main render function, featuring the animation and selective updating
        :return: None
        """

        # Fill the screen and draw the grid if "all" is on
        if self.draw_new["all"]:
            self.window.fill(config.color_bg)
            self.window.blit(self.grid, (0, 0))

        # Calculate the amount the rects change per frame
        ani_diff_w = (self.cw - 3) / config.animate_count / 2
        ani_diff_h = (self.ch - 3) / config.animate_count / 2

        rects = []

        # If animating is enabled, animate the cells dying and reproducing
        if self.animate_switch and config.animate_master:
            # Split the rendering into self.ani_count steps
            for n in range(config.animate_count):
                rects = []

                # Iterate through marked cells, or all cells if "all" flag is on
                for i, j in self.draw_new["cells"] if not self.draw_new["all"] else np.ndindex(self.map.shape):
                    full_rect = (self.cw * j + 2, self.ch * i + 2, self.cw - 3, self.ch - 3)

                    if self.map[i, j]:
                        # Define the rect to draw, taking into account the frame of animation
                        rect = (
                            self.cw * j + 2 + ani_diff_w * (config.animate_count - n),
                            self.ch * i + 2 + ani_diff_h * (config.animate_count - n),
                            self.cw - 3 - ani_diff_w * (config.animate_count - n) * 2,
                            self.ch - 3 - ani_diff_h * (config.animate_count - n) * 2
                        )

                        pygame.draw.rect(self.window.window, config.color_cell_alive, rect)
                        rects.append(rect)
                    else:
                        # Similarly define the rect, just the opposite of the expanding rect
                        rect = (
                            self.cw * j + 2 + ani_diff_w * n,
                            self.ch * i + 2 + ani_diff_h * n,
                            self.cw - 3 - ani_diff_w * n * 2,
                            self.ch - 3 - ani_diff_h * n * 2
                        )

                        # Draw both the surrounding rect to remove the white, then draw the new rect
                        pygame.draw.rect(self.window.window, config.color_cell_dead, full_rect)
                        pygame.draw.rect(self.window.window, config.color_cell_alive, rect)
                        rects.append(full_rect)

                # Update the rects that have been drawn to, then sync the framerate of the animation
                self.window.update(rects)
                self.animate_clock.tick(config.game_speed * config.animate_count * config.animate_speed)

        rects = []

        # Draw the completed scene one more time, to ensure continuity with actual game
        for i, j in self.draw_new["cells"] if not self.draw_new["all"] else np.ndindex(self.map.shape):
            rect = (self.cw * j + 2, self.ch * i + 2, self.cw - 3, self.ch - 3)

            if self.map[i, j]:
                pygame.draw.rect(self.window.window, config.color_cell_alive, rect)
            else:
                pygame.draw.rect(self.window.window, config.color_cell_dead, rect)

            rects.append(rect)

        # Update part of the image, if "all" flag is on, update the whole
        if self.draw_new["all"]:
            self.window.update()
        else:
            self.window.update(rects)

        # Reset the per-frame parameters
        self.draw_new["all"] = False
        self.draw_new["cells"].clear()

    def play(self):
        """
        This function runs the game of life.
        :return: None
        """

        running = True
        self.render()

        while running:
            # update the game, sync the framerate and render the scene
            self.game_tick()
            self.clock.tick(config.game_speed)
            self.render()

            # Iterate through the events pygame collected
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # If user presses escape, stop running the game
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    # Increase the speed
                    elif event.key == pygame.K_UP:
                        config.game_speed *= 1.1

                    # Decrease the speed
                    elif event.key == pygame.K_DOWN:
                        config.game_speed /= 1.1

                    # Jump one frame forward
                    elif event.key == pygame.K_RIGHT:
                        self.game_tick()

                        # Disable the animation, and quickly render the next frame
                        self.animate_switch = False
                        self.render()
                        self.animate_switch = True

    # The main function that triggers when the game starts
    def run(self):
        """
        The main function that should be called when starting the game,
        an editor that allows one to mark cells dead or alive.
        :return: None
        """

        running = True

        while running:
            self.render()

            # Get the x and y position of the mouse, and calculate the indexes of the map
            x, y = pygame.mouse.get_pos()
            buttons = pygame.mouse.get_pressed()

            i = y // self.ch
            j = x // self.cw

            # Only continue if the mouse is inside the map
            if 0 <= i < config.h and 0 <= j < config.w:
                # If left mouse-button has been pressed, mark the cell as alive
                if buttons[0]:
                    if not self.map[i, j]:
                        self.map[i, j] = 1
                        self.draw_new["cells"].append((i, j))

                # If right mouse-button has been pressed, mark the cell as dead
                elif buttons[2]:
                    if self.map[i, j]:
                        self.map[i, j] = 0
                        self.draw_new["cells"].append((i, j))

            # Iterate through the event pygame has collected
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # If the user has pressed escape, close the game
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    # If the player has pressed r, run the game of life
                    elif event.key == pygame.K_r:
                        self.animate_switch = True
                        self.play()
                        self.animate_switch = False

                    # Increase the speed
                    elif event.key == pygame.K_UP:
                        config.game_speed *= 1.1

                    # Decrease the speed
                    elif event.key == pygame.K_DOWN:
                        config.game_speed /= 1.1

                    # If the player presses q, reload the map, thus wiping all cells
                    elif event.key == pygame.K_q:
                        self.map: np.ndarray = np.zeros((config.h, config.w), dtype="bool")
                        self.refresh_neighbors()
                        self.draw_new["all"] = True
