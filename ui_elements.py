import pygame
from typing import Tuple


def align(rect: pygame.Rect, alignment: str):
    if alignment[1] == "l":
        rect.left = rect.x

    elif alignment[1] == "c":
        rect.centerx = rect.x

    else:
        rect.right = rect.x

    if alignment[0] == "t":
        rect.top = rect.y

    elif alignment[0] == "c":
        rect.centery = rect.y

    else:
        rect.bottom = rect.y


class TextField:
    def __init__(self,
                 text: str,
                 font: pygame.font.Font,
                 pos: Tuple[int, int],
                 alignment: str = "cc",
                 text_color: Tuple[int, int, int] = None
                 ):

        # Save all the variables
        self.text = text
        self.font = font
        self.alignment = alignment
        self.pos = pos

        # If text_color not specified
        self.text_color = text_color
        if not self.text_color:
            self.text_color = (0, 0, 0)

        # Create the text surface and rect for rendering
        self.create_text()

    # noinspection PyAttributeOutsideInit
    def create_text(self):
        """
        This function creates the text surface and rect, used in rendering.
        :return: None
        """

        # Call font.render to get the surface
        self.surf = self.font.render(self.text, True, self.text_color)

        # Default to topleft, so that x and y may be correct. Then align the text based on alignment.
        self.rect = self.surf.get_rect(topleft=self.pos)
        align(self.rect, self.alignment)

    def render(self, surface: pygame.Surface, redraw: bool = False):
        """
        This function renders the text onto the given surface,
        at the position specified by self.rect.
        :param surface: A pygame surface to render to
        :param redraw: Determine whether to refresh text before drawing
        :return: None
        """

        if redraw:
            self.create_text()

        # Draw the text surface on the given surface
        surface.blit(self.surf, self.rect)


class Toggle(pygame.Rect):
    def __init__(self,
                 font: pygame.font.Font,
                 color_enabled: Tuple[int, int, int],
                 rect: Tuple[float, float, float, float],
                 alignment: str = "cc",
                 corner_round: int = 2,
                 border_width: int = 2,
                 border_color: Tuple[int, int, int] = None,
                 text_color_enabled: Tuple[int, int, int] = None,
                 text_color_disabled: Tuple[int, int, int] = None
                 ):
        """
        This class emulates a toggle switch,
        in case of boolean variables.

        :param font: The font used to display on and off
        :param color_enabled: The color to use in the enabled cell
        :param rect: The overall rect of the toggle
        :param alignment: The alignment to use
        :param corner_round: The amount of corner rounding
        :param border_width: The width of the border
        :param border_color: The color of the border
        :param text_color_enabled: The color of text in the enabled cell
        :param text_color_disabled: The color of text in the disabled cell
        """

        # Initialize the super, in this case the container rect
        super().__init__(*rect)

        # Save all of the variables used in the class
        self.font = font
        self.color_enabled = color_enabled
        self.alignment = alignment,
        self.corner_round = corner_round
        self.border_width = border_width

        # If no border_color specified, default
        self.border_color = border_color
        if not border_color:
            self.border_color = (0, 0, 0)

        # If no text_color_enabled specified, default
        self.text_color_enabled = text_color_enabled
        if not text_color_enabled:
            self.text_color_enabled = (255, 255, 255)

        # If no text_color_disabled specified, default
        self.text_color_disabled = text_color_disabled
        if not text_color_disabled:
            self.text_color_disabled = (0, 0, 0)

        # Align the rect according to alignment
        align(self, alignment)

        # Initialize the sub rects, the on and off rect
        self.on_rect = pygame.Rect(self.x, self.y, self.centerx - self.x, self.height)
        self.off_rect = pygame.Rect(self.centerx, self.y, self.right - self.centerx, self.height)

        # Initialize the labels associated with the on and off rects
        self.on_label = TextField("on", self.font, self.on_rect.center, text_color=self.text_color_disabled)
        self.off_label = TextField("off", self.font, self.off_rect.center, text_color=self.text_color_enabled)

        # Default to enabled
        self.enabled = False

    def flip(self):
        """
        This function flips the toggle.
        :return: None
        """

        self.enabled = not self.enabled
        self.swap()

    def enable(self):
        """
        This function enables the toggle.
        :return: None
        """

        self.enabled = True
        self.swap()

    def disable(self):
        """
        This function disables the toggle.
        :return: None
        """

        self.enabled = False
        self.swap()

    def swap(self):
        """
        This function swaps the colors of the two labels,
        and forces them to redraw text.
        :return: None
        """
        self.on_label.text_color, self.off_label.text_color = self.off_label.text_color, self.on_label.text_color

        self.on_label.create_text()
        self.off_label.create_text()

    def render(self, surface: pygame.Surface):
        """
        Render the toggle.
        This means rendering the container,
        the two sub-rects and the labels.
        :param surface: The pygame.Surface to draw on
        :return: None
        """

        # Draw the containing rects border
        pygame.draw.rect(surface, self.border_color, self, self.border_width, self.corner_round)

        # Draw the colored rect, indicating whether the toggle is on or off
        pygame.draw.rect(surface, self.color_enabled, self.on_rect if self.enabled else self.off_rect, 0, self.corner_round)

        # Render the labels
        self.on_label.render(surface)
        self.off_label.render(surface)


class Button(pygame.Rect):
    def __init__(self,
                 text: str,
                 font: pygame.font.Font,
                 color: Tuple[int, int, int],
                 callback,
                 rect: Tuple[float, float, float, float],
                 alignment: str = "cc",
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
        :param alignment: A string representing the x and y alignment
        :param corner_round: An int of how much rounding to use on the corners
        :param border_width: An int of how wide to make the border
        :param border_color: A tuple of the color of the border
        :param text_color: A tuple of the color of the text
        """

        # Call the super init to initialize the rect
        super().__init__(*rect)

        # Save all the variables used in the class
        self.color = color
        self.corner_round = corner_round
        self.border_width = border_width
        self.alignment = alignment
        self.callback = callback

        # Default if no border_color specified
        self.border_color = border_color
        if not border_color:
            self.border_color = (50, 50, 50)

        # Default if no text_color specified
        if not text_color:
            text_color = (0, 0, 0)

        # Align the button, according to input
        align(self, alignment)

        # Create the text_field to draw
        self.text_field = TextField(text, font, self.center, text_color=text_color)

    def render(self, surface: pygame.Surface):
        """
        Render the button onto a given surface.
        :param surface: The pygame.Surface to draw on
        :return: None
        """

        # Draw the button and it's border
        pygame.draw.rect(surface, self.color, self, 0, self.corner_round)
        pygame.draw.rect(surface, self.border_color, self, self.border_width, self.corner_round)

        # Draw the text
        self.text_field.render(surface)


class InputBox(pygame.Rect):
    def __init__(self,
                 text: str,
                 content_type: type,
                 font: pygame.font.Font,
                 color: Tuple[int, int, int],
                 rect: Tuple[float, float, float, float],
                 alignment: str = "cc",
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
        :param alignment: A string representing the alignment to use
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
        self.alignment = alignment
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

        # Align the box, according to input
        align(self, alignment)

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
        This function also takes into account the size of the text_surface,
        aligning it to the left and right depending on it's size.
        :param surface: The pygame.Surface to draw on
        :return: None
        """

        # Draw the button and it's border
        pygame.draw.rect(surface, self.color, self, 0, self.corner_round)
        pygame.draw.rect(surface, self.border_color_activated if self.activated else self.border_color, self, self.border_width, self.corner_round)

        # Create the text surface
        text_surf = self.font.render(self.text, True, self.text_color)

        # Get the initial dimensions of the text surface
        text_rect = text_surf.get_rect()
        text_rect_width = text_rect.width
        text_rect_height = text_rect.height

        # If the text surface is too big to fit into the box
        if text_rect_width > self.width - 10:
            # Resize the surface, aligning the text to the right
            sub_surf = text_surf.subsurface((text_rect_width - self.width + 10, 0, self.width - 10, text_rect_height))
            text_rect = sub_surf.get_rect(right=self.right - 5, centery=self.centery)

            # Overwrite initial surface
            text_surf = sub_surf
        else:
            # If not, align the text to the left
            text_rect = text_surf.get_rect(left=self.left + 5, centery=self.centery)

        # Draw the text to the screen
        surface.blit(text_surf, text_rect)
