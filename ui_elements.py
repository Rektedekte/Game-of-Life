import pygame
from typing import Tuple


class Button(pygame.Rect):
    def __init__(self,
                 text: str,
                 font: pygame.font.Font,
                 color: Tuple[int, int, int],
                 callback,
                 rect: Tuple[float, float, float, float],
                 center: bool = True,
                 corner_round: int = 2,
                 border_width: int = 2,
                 border_color: Tuple[int, int, int] = None,
                 text_color: Tuple[int, int, int] = None
                 ):
        """
        This class acts as an abstraction of all the code used to create a button,
        derived from the pygame.Rect class.

        :param text: str of the text to be displayed
        :param font: pygame.font.Font to be used for the text
        :param color: The color of the button
        :param callback: The callback to be called when pressed
        :param rect: The rect tuple to pass to super
        :param center: A bool on whether to center the rect or not
        :param corner_round: An int of how much rounding to use on the corners
        :param border_width: An int of how wide to make the border
        :param border_color: A tuple of the color of the border
        :param text_color: A tuple of the color of the text
        """

        # Call the super init to initialize the rect
        super().__init__(*rect)

        # Save all the variables used in the class
        self.text = text
        self.font = font
        self.color = color
        self.corner_round = corner_round
        self.border_width = border_width
        self.is_centered = center
        self.callback = callback

        # Default if no border_color specified
        self.border_color = border_color
        if not border_color:
            self.border_color = (50, 50, 50)

        # Default if no text_color specified
        self.text_color = text_color
        if not text_color:
            self.text_color = (0, 0, 0)

        # Center the rect if specified
        if center:
            self.center = (self.x, self.y)

    def render(self, surface: pygame.Surface):
        """
        Render the button onto a given surface.
        :param surface: The pygame.Surface to draw on
        :return: None
        """

        # Draw the button and it's border
        pygame.draw.rect(surface, self.color, self, 0, self.corner_round)
        pygame.draw.rect(surface, self.border_color, self, self.border_width, self.corner_round)

        # Draw the text, centering it to the rect
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.center)
        surface.blit(text_surf, text_rect)


class InputBox(pygame.Rect):
    def __init__(self,
                 text: str,
                 content_type: type,
                 font: pygame.font.Font,
                 color: Tuple[int, int, int],
                 rect: Tuple[float, float, float, float],
                 center: bool = True,
                 corner_round: int = 2,
                 border_width: int = 2,
                 border_color: Tuple[int, int, int] = None,
                 border_color_activated: Tuple[int, int, int] = None,
                 text_color: Tuple[int, int, int] = None
                 ):
        """
        This class acts as an abstraction of all code involved in creating an input container.
        It is also derived from the pygame.Rect class.

        :param text: The initial text for the box to contain
        :param content_type: The type of input to be used (str, int, float)
        :param font: the pygame.font.Font to be used in rendering
        :param color: A tuple containing color of the box
        :param rect: A tuple containing the rect of the box
        :param center: A bool on whether to center the rect
        :param corner_round: An int on the roundness of the corners
        :param border_width: An int on the width of the border
        :param border_color: A tuple on the color of the border
        :param border_color_activated: A tuple on the color of the border when activated
        :param text_color: A tuple on the color of the text
        """

        # Call the super init to initialize the rect
        super().__init__(*rect)

        # Save all the variables used in the class
        self.text = text
        self.content_type = content_type
        self.font = font
        self.color = color
        self.corner_round = corner_round
        self.border_width = border_width
        self.is_centered = center
        self.activated = False

        if not self.check():
            raise ValueError("InputBox failed initial value check, ensure correct content_type")

        # Default if no border_color specified
        self.border_color = border_color
        if not border_color:
            self.border_color = (50, 50, 50)

        # Default if no border_color_activated specified
        self.border_color_activated = border_color_activated
        if not self.border_color_activated:
            self.border_color_activated = (220, 20, 20)

        # Default if no text_color specified
        self.text_color = text_color
        if not text_color:
            self.text_color = (0, 0, 0)

        # Center the rect if specified
        if center:
            self.center = (self.x, self.y)

    def check(self):
        """
        This function chooses the correct checker, then returns the result
        :return: The validity as a bool
        """

        return InputBox.checks[self.content_type](self)

    def check_int(self):
        """
        Check whether the text content is valid for int type
        :return: The validity as a bool
        """

        try:
            int(self.text)
        except ValueError:
            return not len(self.text)

        return True

    def check_float(self):
        """
        Check whether the text content is valid for float type
        :return: The validity as a bool
        """

        try:
            float(self.text)
        except ValueError:
            return not len(self.text)

        return True

    # A dict used to jump to the correct checker, can be expanded
    checks = {
        str: lambda self: True,
        int: check_int,
        float: check_float
    }

    def send_keys(self, *keys):
        """
        This function takes *args of keys, and interprets them, changing the text based on it.
        :param keys: A packed tuple of key inputs to interpret
        :return: None
        """

        # Iterate through the keys given
        for key in keys:
            # If the used has pressed backspace
            if key == pygame.K_BACKSPACE:
                if self.text:
                    self.text = self.text[:-1]

            # I the input is a string
            elif isinstance(key, str):
                # Store the original temporarily
                temp = self.text
                self.text += key

                # Check the validity of the new input
                if not self.check():
                    # Reasign if not valid
                    self.text = temp

            # If an invalid input is given, raise an error (thus crashing the program)
            else:
                raise TypeError(f"Type {type(key)} not supported")

    def render(self, surface: pygame.Surface):
        """
        Render the button onto a given surface.
        :param surface: The pygame.Surface to draw on
        :return: None
        """

        # Draw the button and it's border
        pygame.draw.rect(surface, self.color, self, 0, self.corner_round)
        pygame.draw.rect(surface, self.border_color_activated if self.activated else self.border_color, self, self.border_width, self.corner_round)

        # Draw the text, centering it to the rect
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.center)
        surface.blit(text_surf, text_rect)
