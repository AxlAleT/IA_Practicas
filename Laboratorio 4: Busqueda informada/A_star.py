import heapq

def A_star(initial_node, solution, operators, operator_names, heuristic):
    """Implementation of the A* search algorithm."""
    frontier = []
    heapq.heappush(frontier, (0, initial_node))  # (priority, node)
    visited = set()
    parents = {tuple(map(tuple, initial_node)): None}
    costs = {tuple(map(tuple, initial_node)): 0}
    moves = []

    while frontier:
        _, current_node = heapq.heappop(frontier)

        if current_node == solution:
            path = []
            while current_node:
                path.append(current_node)
                current_node = parents[tuple(map(tuple, current_node))]
            return path[::-1], moves

        visited.add(tuple(map(tuple, current_node)))

        for i, operator in enumerate(operators):
            child_node = operator(current_node)
            child_tuple = tuple(map(tuple, child_node))

            if child_tuple not in visited:
                new_cost = costs[tuple(map(tuple, current_node))] + 1  # Increment cost for each move
                if child_tuple not in costs or new_cost < costs[child_tuple]:
                    costs[child_tuple] = new_cost
                    priority = new_cost + heuristic(child_node, solution)  # A* priority function
                    heapq.heappush(frontier, (priority, child_node))
                    parents[child_tuple] = current_node
                    moves.append(operator_names[i])

    return None, []