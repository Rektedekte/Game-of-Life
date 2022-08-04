# Game-of-Life
A pygame game replicating the rules of John Conway's famous Game of Life.

## Installation
```
git clone https://github.com/Rektedekte/Game-of-Life.git
cd Game-of-Life
pip install -r requirements.txt
```

## Running
```
python main.py
```

## Config
The game features a range of adjustable parameters,
both concerning the game map, the rendering of the game,
and the visuals of the ui.

Some visual settings, such as those affecting buttons,
may only be applied after restarting the game.

The most notable settings are:

- Animate: Toggles the animation feature (may run faster without).
- Game-speed: Adjusts the overall speed of the game, can also be adjusted locally within the game.
- Animation frames: The amount of frames involved in a transition (Will run faster with less).
- Animation speed: The speed at which the animation frames are drawn.

## Scaling
The ui is built to scale with the resolution of the primary display.
This should work across all modern resolutions, 
but older or more obscure resolutions are not guaranteed.
