import pygame
import fonts


class Button(pygame.Rect):
    def __init__(self,
                 text: str,
                 font: pygame.font.Font,
                 color: tuple, callback,
                 rect: tuple,
                 center: bool = True,
                 corner_round: int = 2,
                 border_width: int = 2,
                 border_color: tuple = None,
                 text_color: tuple = None
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
            self.center = rect[0:2]

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
