import numpy as np
import cv2
import imutils
from config import DIRECTION_VALUE_TO_NAME_DICT

def safe_slicing(slice_index, max_value):
    return min(max(0, slice_index), max_value)

def safe_img_slicing(img, slice_1_start, slice_1_end, slice_2_start, slice_2_end):
    if slice_1_end < slice_1_start:
        slice_1_start, slice_1_end = slice_1_end, slice_1_start
        
    if slice_2_end < slice_2_start:
        slice_2_start, slice_2_end = slice_2_end, slice_2_start
        
    h_max, w_max = img.shape[0] - 1, img.shape[1] - 1 # indexing starts at 0

    return img[safe_slicing(slice_1_start, h_max) : safe_slicing(slice_1_end, h_max) + 1, safe_slicing(slice_2_start, w_max) : safe_slicing(slice_2_end, w_max) + 1]


class MazeState:
    """
    A state tells us two things:
        - the position of the player
        - the layout of the maze.
    Since the latter does not change depending on the player's position, it makes sense to make it static to reduce memory usage.
    """

    MAZE_LAYOUT = None # 3D array, where each value in the list at the [i, j]-th position is a list of the available actions (e.g. left, right) for that specific maze cell.
    
    def __init__(self, player_position=(0,0)):
        self.player_position = player_position

    def equals(self, other_state):
        return self.player_position == other_state.player_position

class SearchNode:
    def __init__(self, state, parent, operator, depth):
        self.state = state
        self.parent = parent
        self.operator = operator
        self.depth = depth

class MazeOperator:
    def __init__(self, direction: tuple):
        self.direction = direction

    def can_be_used(self, state):
        return self.direction in MazeState.MAZE_LAYOUT[state.player_position[1], state.player_position[0]]

    def use(self, state: MazeState):
        return MazeState((state.player_position[0] + self.direction[0], state.player_position[1] + self.direction[1]))


class BreadthFirstSearchAlgorithm:
    def __init__(self, start_state, operators):
        self.start_state = start_state
        self.operators = operators

    def execute(self):
        start_node = SearchNode(state=self.start_state, parent=None, operator=None, depth=0)

        open_nodes = {start_node}
        closed_nodes = set()

        while True:
            if len(open_nodes) == 0:
                break

            min_depth = min([n.depth for n in open_nodes])

            node = [n for n in open_nodes if n.depth == min_depth][0]

            if self.is_goal_state(node.state):
                break

            for o in self.operators:
                if o.can_be_used(node.state):
                    new_state = o.use(node.state)

                    is_in_open_nodes = len([True for n in open_nodes if n.state.equals(new_state)]) != 0
                    is_in_closed_nodes = len([True for n in closed_nodes if n.state.equals(new_state)]) != 0

                    if not is_in_open_nodes and not is_in_closed_nodes:
                        new_node = SearchNode(state=new_state, parent=node, operator=o, depth=node.depth + 1)
                        open_nodes.add(new_node)

            open_nodes.remove(node)
            closed_nodes.add(node)

        if len(open_nodes) > 0:
            print("Found solution.")

            # The operators used to produce the goal state form the solution.
            solution = []

            while node != None:
                solution.append(node.operator)

                node = node.parent
            
            solution = solution[::-1][1:] # We don't need the operator of the start state (which is None).

            print("The solution is:")
            print(" -> ".join([DIRECTION_VALUE_TO_NAME_DICT[op.direction] for op in solution]))

            return solution
        else:
            print("Did not find solution.")
            return None
        
    def is_goal_state(self, state):
        return True

class MazeBreadthFirstSearchAlgorithm(BreadthFirstSearchAlgorithm):
    def __init__(self, start_state, operators, goal_cell_position: tuple):
        super().__init__(start_state, operators)

        self.goal_cell_position = goal_cell_position

    def is_goal_state(self, state: MazeState):
        return state.player_position == self.goal_cell_position