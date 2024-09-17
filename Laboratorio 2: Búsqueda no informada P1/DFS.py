def DFS(initial_node, solution, operators, operator_names):
    """Implementation of the Depth-First Search (DFS) algorithm."""
    frontier, visited, parents = [initial_node], [], {tuple(map(tuple, initial_node)) if isinstance(initial_node[0], list) else tuple(initial_node): None}
    moves = []

    while frontier:
        current_node = frontier.pop()

        if current_node == solution:
            path = []
            while current_node:
                path.append(current_node)
                current_node = parents[tuple(map(tuple, current_node)) if isinstance(current_node[0], list) else tuple(current_node)]
            return path[::-1], moves

        visited.append(current_node)
        for i, operator in enumerate(operators):
            child_node = operator(current_node)
            if child_node not in visited and child_node not in frontier:
                frontier.append(child_node)
                parents[tuple(map(tuple, child_node)) if isinstance(child_node[0], list) else tuple(child_node)] = current_node
                moves.append(operator_names[i])

    return None, []


def swap(arr, i, j):
    """Swaps the elements at positions i and j in the list."""
    new_arr = arr[:]
    new_arr[i], new_arr[j] = new_arr[j], new_arr[i]
    return new_arr

# Creating swap operators for the puzzle
def swap_0_1(arr): return swap(arr, 0, 1)
def swap_1_2(arr): return swap(arr, 1, 2)
def swap_2_3(arr): return swap(arr, 2, 3)

# Puzzle 4 definition
puzzle4 = [4, 2, 3, 1]
operators4 = [swap_0_1, swap_1_2, swap_2_3]
operator_names4 = ['swap_0_1', 'swap_1_2', 'swap_2_3']

def find_position(matrix, target=2):
    """Finds the position of the 'target' value in the matrix."""
    for i, row in enumerate(matrix):
        if target in row:
            return (i, row.index(target))
    return None

def is_within_bounds(pos, matrix):
    """Checks if a position is within the bounds of the matrix."""
    return 0 <= pos[0] < len(matrix) and 0 <= pos[1] < len(matrix[0])

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

# Defining movement operators
def move_up(matrix): return move(matrix, lambda pos: (pos[0] - 1, pos[1]))
def move_down(matrix): return move(matrix, lambda pos: (pos[0] + 1, pos[1]))
def move_left(matrix): return move(matrix, lambda pos: (pos[0], pos[1] - 1))
def move_right(matrix): return move(matrix, lambda pos: (pos[0], pos[1] + 1))

# Labyrinth definition
# 0 = path, 1 = wall, 2 = starting position
labyrinth_puzzle = [
    [1, 2, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1]
]

labyrinth_solution = [
    [1, 0, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1],
    [1, 0, 0, 0, 2],
    [1, 1, 1, 1, 1]
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


# Running the code for the labyrinth
path, moves = DFS(labyrinth_puzzle, labyrinth_solution, labyrinth_operators, labyrinth_operator_names)
print("Path and moves for the labyrinth:")
print_path_and_moves(path, moves)

# Running the code for puzzle 4
path4, moves4 = DFS(puzzle4, [1, 2, 3, 4], operators4, operator_names4)
print("\nPath and moves for puzzle 4:")
print_path_and_moves(path4, moves4)
