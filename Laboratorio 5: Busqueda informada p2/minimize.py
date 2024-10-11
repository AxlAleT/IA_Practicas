import numpy as np

def himmelblau(x, y):
    return (x**2 + y - 11)**2 + (x + y**2 - 7)**2

def minimize(function, min_val, max_val, rate_of_change, iterations):
    reduction_factor = rate_of_change
    radius = max_val - min_val
    # Initial random point
    point = np.random.uniform(min_val, max_val, size=2)

    while radius > 0 and iterations > 0:
        f_point = function(point[0], point[1])
        
        # Generate 8 new points around the current one
        new_points = [point + np.array([dx, dy]) * radius 
                      for dx in [-1, 1] for dy in [-1, 1]]
        
        # Evaluate all the new points
        best_new_point = min(new_points, key=lambda p: function(p[0], p[1]))
        
        # If we find a better point, we take it
        if function(best_new_point[0], best_new_point[1]) < f_point:
            point = best_new_point
        else:
            # Try a random point as a safety measure against local minima
            random_point = np.random.uniform(min_val, max_val, size=2)
            if function(random_point[0], random_point[1]) < f_point:
                point = random_point
        
        # Reduce the radius (controlled by the rate of change) and decrease iterations
        radius = radius - reduction_factor
        iterations -= 1

    return point, iterations

# Example usage
min_val = -5
max_val = 5
rate_of_change = 0.001
iterations = 10000

minimum, remaining_iterations = minimize(himmelblau, min_val, max_val, rate_of_change, iterations)
print("Minimum found:", minimum, "After", iterations - remaining_iterations, "iterations")
