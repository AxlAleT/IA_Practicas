import numpy as np

def himmelblau(x, y):
    return (x**2 + y - 11)**2 + (x + y**2 - 7)**2

def simulated_annealing(function, min_val, max_val, initial_temp, cooling_rate, iterations):
    # Initial random point
    point = np.random.uniform(min_val, max_val, size=2)
    best_point = point
    best_value = function(point[0], point[1])
    
    temperature = initial_temp

    while temperature > 0.1 and iterations > 0:
        f_point = function(point[0], point[1])
        
        # Generate a new random point within a neighborhood
        new_point = point + np.random.uniform(-1, 1, size=2)
        new_point = np.clip(new_point, min_val, max_val)  # Ensure it stays within bounds
        f_new_point = function(new_point[0], new_point[1])
        
        # Acceptance criteria
        if f_new_point < f_point:
            point = new_point
        else:
            # Accept worse solutions with a probability based on temperature
            prob_accept = np.exp(-(f_new_point - f_point) / temperature)
            if np.random.rand() < prob_accept:
                point = new_point
        
        # Update best point found
        if f_new_point < best_value:
            best_value = f_new_point
            best_point = new_point

        # Cool down temperature
        temperature *= cooling_rate
        iterations -= 1

    return best_point, best_value

# Example usage
min_val = -5
max_val = 5
initial_temp = 1000
cooling_rate = 0.99
iterations = 10000

minimum, value = simulated_annealing(himmelblau, min_val, max_val, initial_temp, cooling_rate, iterations)
print("Minimum found:", minimum, "with value", value)
