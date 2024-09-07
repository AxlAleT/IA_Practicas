import random
import sys

mini = -4.5
max = 4.5
iteraciones = 10000

def funcion(x, y):
    return (1.5 - x + x * y) ** 2 + (2.25 - x + x * y ** 2) ** 2 + (2.625 - x + x * y ** 3) ** 2

def random_value():
    return random.uniform(mini, max)

if __name__ == "__main__":
    minimo = sys.float_info.max
    Xminimo, Yminimo = sys.float_info.max, sys.float_info.max
    for i in range(iteraciones):
        Xa = random_value()
        Ya = random_value()
        z = funcion(Xa, Ya)
        if z < minimo:
            minimo = z
            Xminimo = Xa
            Yminimo = Ya

    print("El minimo es: ", minimo, "en X: ", Xminimo, "y Y: ", Yminimo)