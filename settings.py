"""
This file contains the settings class, which operates the settings menu.
This file modifies the config.json file, which in turn is used by the entire program through the Config class.
"""

import pygame

import fonts
from config import config
from ui_elements import Button, TextField, InputBox, Toggle, InputGroup


class Settings:
    def __init__(self, window):
        self.window = window
        self.window.resize(int(self.window.scale_x(700)), int(self.window.scale_y(900)), False)
        self.window.set_caption("Settings - Game of Life")
        self.clock = pygame.time.Clock()

        text_default = {
            "font": fonts.main,
            "alignment": "cl",
            "text_color": config.color_text
        }

        self.text_fields = []

        text_contents = (
            "GAME SETTINGS",
            "Width:",
            "Height:",
            "",
            "ANIMATION SETTINGS",
            "Game-speed:",
            "Animate:",
            "Animation frames:",
            "Animation speed:",
            "",
            "COLOR SETTINGS",
            "Background color:",
            "Live cell color:",
            "Dead cell color:",
            "Grid color:",
            "Button color:",
            "Button border color:",
            "Button text color:",
            "Text color:"
        )

        for text, i in zip(text_contents, range(len(text_contents))):
            self.text_fields.append(TextField(text, pos=self.window.scale_xy(20, i * 40 + 35), **text_default))

        self.input_fields = []
        self._load_config()

        self.buttons = []

        self.buttons.append(Button(
            "exit",
            fonts.main,
            config.color_buttons,
            self.exit,
            self.window.scale_rect((60, 800, 180, 80)),
            "tl"
        ))

        self.buttons.append(Button(
            "save",
            fonts.main,
            config.color_buttons,
            self.save,
            self.window.scale_rect((260, 800, 180, 80)),
            "tl"
        ))

        self.buttons.append(Button(
            "reset",
            fonts.main,
            config.color_buttons,
            self.reset,
            self.window.scale_rect((460, 800, 180, 80)),
            "tl"
        ))

        # Send keys refers to the function that takes keys in the activated input field
        self.send_keys = None

        # To send keys to the input fields, we use a buffer that collects presses
        self.input_buffer = []

        # For this class, we use a running variable available to the entire object
        self.running = True

    def _load_config(self):
        """
        This function loads the config.
        It is painful to have this much init code in a class function,
        but it is necessary for the reset function.

        :return: None
        """

        self.input_fields.clear()

        self.input_fields.append(InputBox(
            config.w,
            int,
            fonts.main,
            (240, 240, 240),
            self.window.scale_rect((680, 75, 100, 38)),
            "cr",
            text_color=config.color_buttons_text,
            border_color=config.color_buttons_border
        ))

        self.input_fields.append(InputBox(
            config.h,
            int,
            fonts.main,
            (240, 240, 240),
            self.window.scale_rect((680, 115, 100, 38)),
            "cr",
            text_color=config.color_buttons_text,
            border_color=config.color_buttons_border
        ))

        self.input_fields.append(InputBox(
            config.game_speed,
            float,
            fonts.main,
            (240, 240, 240),
            self.window.scale_rect((680, 235, 100, 38)),
            "cr",
            text_color=config.color_buttons_text,
            border_color=config.color_buttons_border
        ))

        self.input_fields.append(Toggle(
            fonts.main,
            config.color_buttons_border,
            self.window.scale_rect((680, 275, 200, 38)),
            "cr",
            border_color=config.color_buttons_border,
            enabled=config.animate_master
        ))

        self.input_fields.append(InputBox(
            config.animate_count,
            int,
            fonts.main,
            (240, 240, 240),
            self.window.scale_rect((680, 315, 100, 38)),
            "cr",
            text_color=config.color_buttons_text,
            border_color=config.color_buttons_border
        ))

        self.input_fields.append(InputBox(
            config.animate_speed,
            float,
            fonts.main,
            (240, 240, 240),
            self.window.scale_rect((680, 355, 100, 38)),
            "cr",
            text_color=config.color_buttons_text,
            border_color=config.color_buttons_border
        ))

        self.input_fields.append(InputGroup(
            config.color_bg,
            int,
            fonts.main,
            (240, 240, 240),
            self.window.scale_rect((680, 475, 244, 38)),
            "cr",
            padding=2,
            text_color=config.color_buttons_text,
            border_color=config.color_buttons_border
        ))

        self.input_fields.append(InputGroup(
            config.color_cell_alive,
            int,
            fonts.main,
            (240, 240, 240),
            self.window.scale_rect((680, 515, 244, 38)),
            "cr",
            padding=2,
            text_color=config.color_buttons_text,
            border_color=config.color_buttons_border
        ))

        self.input_fields.append(InputGroup(
            config.color_cell_dead,
            int,
            fonts.main,
            (240, 240, 240),
            self.window.scale_rect((680, 555, 244, 38)),
            "cr",
            padding=2,
            text_color=config.color_buttons_text,
            border_color=config.color_buttons_border
        ))

        self.input_fields.append(InputGroup(
            config.color_grid,
            int,
            fonts.main,
            (240, 240, 240),
            self.window.scale_rect((680, 595, 244, 38)),
            "cr",
            padding=2,
            text_color=config.color_buttons_text,
            border_color=config.color_buttons_border
        ))

        self.input_fields.append(InputGroup(
            config.color_buttons,
            int,
            fonts.main,
            (240, 240, 240),
            self.window.scale_rect((680, 635, 244, 38)),
            "cr",
            padding=2,
            text_color=config.color_buttons_text,
            border_color=config.color_buttons_border
        ))

        self.input_fields.append(InputGroup(
            config.color_buttons_border,
            int,
            fonts.main,
            (240, 240, 240),
            self.window.scale_rect((680, 675, 244, 38)),
            "cr",
            padding=2,
            text_color=config.color_buttons_text,
            border_color=config.color_buttons_border
        ))

        self.input_fields.append(InputGroup(
            config.color_buttons_text,
            int,
            fonts.main,
            (240, 240, 240),
            self.window.scale_rect((680, 715, 244, 38)),
            "cr",
            padding=2,
            text_color=config.color_buttons_text,
            border_color=config.color_buttons_border
        ))

        self.input_fields.append(InputGroup(
            config.color_text,
            int,
            fonts.main,
            (240, 240, 240),
            self.window.scale_rect((680, 755, 244, 38)),
            "cr",
            padding=2,
            text_color=config.color_buttons_text,
            border_color=config.color_buttons_border
        ))

    def reset(self):
        config.reset()
        self._load_config()

    def exit(self):
        self.running = False
        self.window.resize(None, None, True)
        self.window.set_caption("Game of Life")

    def save(self):
        # Iterate over all config entries in config, and reassign their values
        for i, conf in enumerate(config.content.keys()):
            config.content[conf] = self.input_fields[i].value

        # Save entire config
        config.save()

    def render(self):
        self.window.fill(config.color_bg)

        for text_field in self.text_fields:
            text_field.render(self.window.window)

        for input_field in self.input_fields:
            input_field.render(self.window.window)

        for button in self.buttons:
            button.render(self.window.window)

        self.window.update()

    def run(self):
        """
        This function runs the settings menu
        :return: None
        """

        self.running = True
        self.render()

        while self.running:
            self.render()
            self.clock.tick(24)

            # If an input field is activated, send the buffer and clear
            if self.send_keys:
                self.send_keys(*self.input_buffer)
                self.input_buffer.clear()

            # Iterate through the events pygame has collected
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # If the user has pressed escape, return to the main menu
                    if event.key == pygame.K_ESCAPE:
                        self.exit()

                    # If the user has pressed return, deactivate current input field
                    elif event.key == pygame.K_RETURN:
                        if self.send_keys:
                            self.send_keys(False)

                    # If key input is not recognized, collect the key to buffer
                    else:
                        # If the key is backspace, preserve the event
                        if event.key == pygame.K_BACKSPACE:
                            self.input_buffer.append(event.key)

                        # Otherwise, take the unicode
                        else:
                            self.input_buffer.append(event.unicode)

                # If the user has pressed mouse-button up
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        # Get the position of the cursor
                        x, y = pygame.mouse.get_pos()
                        collision = False

                        # Iterate through input fields
                        for input_field in self.input_fields:
                            # Store collision result
                            new_send_keys = input_field.collidepoint(x, y)

                            # If a collision is detected
                            if new_send_keys:
                                collision = True

                                # If collision occurs on non-text-based input, reset send_keys
                                if isinstance(new_send_keys, bool):
                                    self.send_keys = None

                                # If collision occurs on text-based input, set new send_keys
                                else:
                                    self.send_keys = new_send_keys
                                    self.input_buffer.clear()

                        # If not collision occurs, send_keys must be None
                        if not collision:
                            self.send_keys = None

                        # Iterate through buttons
                        for button in self.buttons:
                            if button.collidepoint(x, y):
                                button.callback()
