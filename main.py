import pyautogui
import time
import cv2
import numpy as np
from utils import safe_img_slicing
import config
import matplotlib.pyplot as plt
from utils import MazeBreadthFirstSearchAlgorithm, MazeState, MazeOperator

DIFFICULTY = config.Difficulty.hard

DIRECTIONS = config.DIRECTIONS
DIRECTION_VALUE_TO_NAME_DICT = config.DIRECTION_VALUE_TO_NAME_DICT

MAZE_TOP_LEFT = config.MAZE_TOP_LEFT[DIFFICULTY]
MAZE_BOTTOM_RIGHT = config.MAZE_BOTTOM_RIGHT[DIFFICULTY]
MAZE_SIZE = config.MAZE_SIZE[DIFFICULTY]
CELL_SIZE = config.CELL_SIZE[DIFFICULTY]
CELL_SIZE_HALVED = config.CELL_SIZE_HALVED[DIFFICULTY]
LOOKAHEAD_LENGTH = config.LOOKAHEAD_LENGTH[DIFFICULTY]
KEY_PRESS_DURATION = config.KEY_PRESS_DURATION[DIFFICULTY]

def take_action(action):
    pyautogui.keyDown(action)
    
    time.sleep(KEY_PRESS_DURATION)
    pyautogui.keyUp(action)

def take_screenshot():
    return np.array(pyautogui.screenshot())[MAZE_TOP_LEFT[1]:MAZE_BOTTOM_RIGHT[1], MAZE_TOP_LEFT[0]:MAZE_BOTTOM_RIGHT[0], :][...,::-1]

def threshold_image(img):
    _, result = thresh1 = cv2.threshold(img, 119, 255, 0)
    return result

def filter_trail_from_image(img):
    indices = np.where(img[:,:,0] < 150)

    img[indices[0], indices[1], :] = 0

    return img

def filter_player_figure_from_image(img):
    img[6:CELL_SIZE, 6:CELL_SIZE] = 0

    return img

def get_maze_layout(img):
    cells = np.zeros((MAZE_SIZE, MAZE_SIZE), dtype=list)

    for row in range(MAZE_SIZE):
        for col in range(MAZE_SIZE):
            cell_center = (col * CELL_SIZE + CELL_SIZE_HALVED, row * CELL_SIZE + CELL_SIZE_HALVED)
            possible_directions_for_cell = []

            # We examine if there is a black wall in each direction.
            for idx, direction in enumerate(DIRECTIONS):
                img_part = safe_img_slicing(img, cell_center[1], cell_center[1] + LOOKAHEAD_LENGTH * direction[1], cell_center[0], cell_center[0] + LOOKAHEAD_LENGTH * direction[0])

                # If there is not a wall in this direction, then we add this to the possible directions from this cell.
                if not np.any(img_part == 255):
                    possible_directions_for_cell.append(DIRECTIONS[idx])
            
            cells[row, col] = possible_directions_for_cell
                 
    return cells

# Some delay to let the user focus on the game window with the mouse.
time.sleep(2)

maze = take_screenshot()

maze = filter_player_figure_from_image(threshold_image(cv2.cvtColor(filter_trail_from_image(maze), cv2.COLOR_BGR2GRAY)))

maze_layout = get_maze_layout(maze)

MazeState.MAZE_LAYOUT = maze_layout
alg = MazeBreadthFirstSearchAlgorithm(start_state=MazeState((0,0)), operators=[MazeOperator(d) for d in DIRECTIONS], goal_cell_position=(MAZE_SIZE - 1, MAZE_SIZE - 1))

solution = alg.execute()

if solution is None:
    print("Could not find solution.")
else:
    for operator in solution:
        action = DIRECTION_VALUE_TO_NAME_DICT[operator.direction]
        
        take_action(action)
        