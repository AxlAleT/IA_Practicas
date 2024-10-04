import random

class MazeGenerator:
    """Generates a random maze and its solution using Depth-First Search (DFS)."""
    
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.maze = [[1 for _ in range(width)] for _ in range(height)]  # Initialize the maze with walls
        self.start = (1, 1)  # Starting point
        self.end = (height - 2, width - 2)  # End point
        self.solution = []  # To store the solution path
    
    def generate_maze(self):
        """Generates the maze and stores it in the maze attribute."""
        self._dfs(self.start[0], self.start[1])
        # Mark the start and end in the final maze
        self.maze[self.start[0]][self.start[1]] = 2  # Mark start with 2
        self.maze[self.end[0]][self.end[1]] = 0  # End point in original maze remains 0
    
    def _dfs(self, x, y):
        """Performs randomized DFS to carve out the maze."""
        # Define the four possible directions: (row_delta, col_delta)
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)  # Randomize the order of exploration

        for dx, dy in directions:
            nx, ny = x + dx, y + dy  # Next cell coordinates
            if 1 <= nx < self.height - 1 and 1 <= ny < self.width - 1 and self.maze[nx][ny] == 1:
                # Carve a path between the current cell and the next one
                self.maze[nx][ny] = 0
                self.maze[x + dx // 2][y + dy // 2] = 0
                self.solution.append((nx, ny))  # Add this cell to the solution path
                self._dfs(nx, ny)
    
    def get_start_maze(self):
        """Returns the maze with the start position marked as '2'."""
        return self.maze

    def get_solution_maze(self):
        """Returns the maze with the end position marked as '2'."""
        solution_maze = [row[:] for row in self.maze]  # Copy the maze
        solution_maze[self.end[0]][self.end[1]] = 2  # Mark the end with '2'
        return solution_maze


def print_maze(maze):
    """Utility function to print the maze."""
    for row in maze:
        print("".join(str(cell) for cell in row))


# Example Usage
height, width = 80, 80  # Define the size of the maze (must be odd numbers for proper maze generation)
generator = MazeGenerator(height, width)
generator.generate_maze()

# Get the start maze and the solution maze
start_maze = generator.get_start_maze()
solution_maze = generator.get_solution_maze()
