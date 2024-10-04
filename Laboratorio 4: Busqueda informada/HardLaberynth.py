import time
import A_star

def heuristic(node, solution):
    """Calculates the Manhattan distance between the '2' in the current node and the solution."""
    pos_node = find_position(node)
    pos_solution = find_position(solution)
    return abs(pos_node[0] - pos_solution[0]) + abs(pos_node[1] - pos_solution[1])

def find_position(matrix, target=2):
    """Finds the position of the 'target' value in the matrix."""
    for i, row in enumerate(matrix):
        if target in row:
            return (i, row.index(target))
    return None

def move(matrix, direction):
    """Moves the '2' in the matrix according to the given direction."""
    pos = find_position(matrix)
    if not pos:
        return matrix

    new_pos = direction(pos)
    if is_within_bounds(new_pos, matrix) and matrix[new_pos[0]][new_pos[1]] == 0:
        new_matrix = [row[:] for row in matrix]
        new_matrix[pos[0]][pos[1]] = 0
        new_matrix[new_pos[0]][new_pos[1]] = 2
        return new_matrix
    return matrix

def is_within_bounds(pos, matrix):
    """Checks if a position is within the bounds of the matrix."""
    return 0 <= pos[0] < len(matrix) and 0 <= pos[1] < len(matrix[0])



# Defining movement operators
def move_up(matrix): return move(matrix, lambda pos: (pos[0] - 1, pos[1]))
def move_down(matrix): return move(matrix, lambda pos: (pos[0] + 1, pos[1]))
def move_left(matrix): return move(matrix, lambda pos: (pos[0], pos[1] - 1))
def move_right(matrix): return move(matrix, lambda pos: (pos[0], pos[1] + 1))

# Labyrinth definition
# 0 = path, 1 = wall, 2 = starting position
labyrinth_puzzle = [
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


labyrinth_solution = [
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 0, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


labyrinth_operators = [move_up, move_down, move_left, move_right]
labyrinth_operator_names = ['move_up', 'move_down', 'move_left', 'move_right']

def print_path_and_moves(path, moves):
    """Prints the path and the moves performed."""
    for i, step in enumerate(path):
        print(f"Step {i}:")
        if isinstance(step[0], list):
            for row in step:
                print(" ".join(map(str, row)))
        else:
            print(step)
        if i < len(moves):
            print(f"Move: {moves[i]}\n")
    

start_time = time.time() 
path, moves = A_star.A_star(labyrinth_puzzle, labyrinth_solution, labyrinth_operators, labyrinth_operator_names, heuristic)
end_time = time.time()

print("Path and moves for the labyrinth with A*:")
print_path_and_moves(path, moves)
print( f"Tiempo de ejecucion: {end_time - start_time}")