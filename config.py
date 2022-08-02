"""
This file contains a simple wrapper for the functionality of the config file.
Other files need simply to import this file, and they will have full access to the initialized config object.
This shaves down tons of redundant code.
"""

import json


class Config:
    def __init__(self):
        """
        The Config class take no parameters,
        as it is already tied to the config.json file.

        Config parameters can be flatly accessed through attributing.
        """

        # Load the config.json file, and parse it with json
        with open("config.json", "r") as f:
            data = json.load(f)

        # Flatten the data to simplify handling
        flatten_data = {
            **data["field-dimensions"],
            "game_speed": data["game-speed"],
            **data["animation"],
            **data["colors"]
        }

        self.content = {}

        # Iterate through and replace dashes with underscores
        for k, v in flatten_data.items():
            self.content[k.replace("-", "_")] = v

    # Get item through attributing
    def __getattr__(self, item):
        return self.content.__getitem__(item)

    # Set item through attributing
    def __setattr__(self, key, value):
        if key == "content":
            self.__dict__[key] = value
        else:
            self.content[key] = value

    def save(self):
        """
        This function saves the config from the parameters to the file.
        It is very manual as of now.
        :return: None
        """

        data = {
            "field-dimensions": {
                "w": self.w,
                "h": self.h
            },
            "game-speed": self.game_speed,
            "animation": {
                "animate-master": self.animate_master,
                "animate-count": self.animate_count,
                "animate-speed": self.animate_speed
            },
            "colors": {
                "color-bg": self.color_bg,
                "color-cell-alive": self.color_cell_alive,
                "color-cell-dead": self.color_cell_dead,
                "color-grid": self.color_grid,
                "color-buttons": self.color_buttons,
                "color-buttons-border": self.color_buttons_border,
                "color-buttons-text": self.color_buttons_text,
                "color-text": self.color_text
            }
        }

        # Dump the content, pretty print style
        with open("config.json", "w") as f:
            json.dump(data, f, indent=4)


config = Config()
