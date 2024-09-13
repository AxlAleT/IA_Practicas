puzzle4 = [4, 2, 3, 1]

i = lambda arr: [arr[1], arr[0]] + arr[2:]
c = lambda arr: arr[:1] + [arr[2], arr[1]] + arr[3:]
d = lambda arr: [arr[0], arr[1], arr[3], arr[2]]
operadores4 = [i, c, d]

def DFS(Nodo_Inicial, Solucion, operadores):
    Nodos_Frontera = []
    Nodos_Visitados = []

    Nodos_Frontera.append(Nodo_Inicial)

    while True:
        try:
            Nodo_Actual = Nodos_Frontera.pop()
        except IndexError:
            break

        if Nodo_Actual == Solucion:
            return Nodo_Actual
        else:
            Nodos_Visitados.append(Nodo_Actual)
            for operador in operadores:
                Nodo_Hijo = operador(Nodo_Actual)
                if Nodos_Visitados.count(Nodo_Hijo) == 0 and Nodos_Frontera.count(Nodo_Hijo) == 0:
                    Nodos_Frontera.append(Nodo_Hijo)

    return None

print(DFS(puzzle4, [1, 2, 3, 4], operadores4))