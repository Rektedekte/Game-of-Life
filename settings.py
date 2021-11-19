import fonts
from config import config
from ui_elements import Button, TextField, InputBox


class Settings:
    def __init__(self, window):
        self.window = window

        text_default = {
            "font": fonts.main,
            "center": False
        }

        self.text_fields = []
        self.text_fields.append(TextField("Width:", pos=(5, 5), **text_default))
        self.text_fields.append(TextField("Height:", pos=(5, 55), **text_default))
        self.text_fields.append(TextField("Game-speed:", pos=(5, 105), **text_default))
        self.text_fields.append(TextField("Animate:", pos=(5, 155), **text_default))
        self.text_fields.append(TextField("Animation frames:", pos=(5, 205), **text_default))
        self.text_fields.append(TextField("Animation speed:", pos=(5, 255), **text_default))
        self.text_fields.append(TextField("Background color:", pos=(5, 305), **text_default))
        self.text_fields.append(TextField("Live cell color:", pos=(5, 355), **text_default))
        self.text_fields.append(TextField("Dead cell color:", pos=(5, 405), **text_default))
        self.text_fields.append(TextField("Grid color:", pos=(5, 455), **text_default))
        self.text_fields.append(TextField("Button color:", pos=(5, 505), **text_default))
        self.text_fields.append(TextField("Button border color:", pos=(5, 555), **text_default))
        self.text_fields.append(TextField("Text color:", pos=(5, 605), **text_default))

    def render(self):
        self.window.fill(config.color_bg)

        for text_field in self.text_fields:
            text_field.render(self.window.window)

        self.window.update()
