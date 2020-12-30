# The values inside this file were calculated with the following settings:
# -1080p monitor
# - Google Chrome
# - 90% zoom level

from enum import Enum  

class Difficulty(Enum):
    easy = 1
    medium = 2
    hard = 3

# These are used to crop the screenshot to the maze.
MAZE_TOP_LEFT = {
    Difficulty.easy: (534, 347),
    Difficulty.medium: (534, 346),
    Difficulty.hard: (499, 313)
}

MAZE_BOTTOM_RIGHT = {
    Difficulty.easy: (1039, 851),
    Difficulty.medium: (1035, 850),
    Difficulty.hard: (1067, 879)
}

# The number of cells in a row/column.
MAZE_SIZE = {
    Difficulty.easy: 10,
    Difficulty.medium: 12,
    Difficulty.hard: 15
}

# The size of each cell in the maze.
CELL_SIZE = {
    Difficulty.easy: 50,
    Difficulty.medium: 42,
    Difficulty.hard: 38
}

# These are stored to speed up the computation a bit (we won't need to calculate these again and again).
CELL_SIZE_HALVED = {
    Difficulty.easy: CELL_SIZE[Difficulty.easy] // 2,
    Difficulty.medium: CELL_SIZE[Difficulty.medium] // 2,
    Difficulty.hard: CELL_SIZE[Difficulty.hard] // 2
}

# The length of the lines in which the agent observes the environment.
LOOKAHEAD_LENGTH = {
    Difficulty.easy: CELL_SIZE_HALVED[Difficulty.easy] + 10,
    Difficulty.medium: CELL_SIZE_HALVED[Difficulty.medium] + 7,
    Difficulty.hard: CELL_SIZE_HALVED[Difficulty.hard] + 5
}

# The duration of any given key being pressed when the agent executes an action (e.g. move left).
KEY_PRESS_DURATION = {
    Difficulty.easy: 0.32,
    Difficulty.medium: 0.25,
    Difficulty.hard: 0.21
}

# This is used to threshold the input image to create a grayscale image in which only the player's figure and the maze remains.
THRESHOLD = 119

# The directions the agent can take.
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Converts the directions to their 'standard' names, e.g 'left', 'right'.
DIRECTION_VALUE_TO_NAME_DICT = {
    (-1, 0): "left",
    (1, 0): "right",
    (0, -1): "up",
    (0, 1): "down"
}