"""
The main script that creates the window and starts the game.
Any modifications to the script-path should be done here.
"""

from game import Game
from window import Window

if __name__ == "__main__":
    window = Window()
    game = Game(window)
    game.run()
    window.close()
