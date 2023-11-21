class Matrix:
    def __init__(self, n):
        self.n = n
        self.rows = [dict() for _ in range(n)]

    def get(self, i, j):
        return self.rows[i].get(j, 0.0)

    def set(self, i, j, val):
        if val:
            self.rows[i][j] = val
        else:
            del self.rows[i][j]

    def add(self, i, j, val):
        self.set(i, j, self.get(i, j) + val)

    def __str__(self):
        out = ""
        for i in range(len(self.rows)):
            for j in range(len(self.rows) + 1):
                out += str(self.get(i, j)) + "\t"
            out += "\n"
        return out


class Node:
    def __init__(self, index, name):
        self.index = index
        self.name = name


class Component:
    def __init__(self):
        pass

    def apply(self, mat: Matrix):
        raise NotImplemented


class Resistor(Component):
    def __init__(self, ohms, a: Node, b: Node):
        super().__init__()
        self.ohms = ohms
        self.a = a
        self.b = b

    def apply(self, mat: Matrix):
        mat.add(self.a.index, self.a.index, 1 / self.ohms)
        mat.add(self.a.index, self.b.index, -1 / self.ohms)
        mat.add(self.b.index, self.a.index, -1 / self.ohms)
        mat.add(self.b.index, self.b.index, 1 / self.ohms)


class CurrentSource(Component):
    def __init__(self, amps, a: Node, b: Node):
        super().__init__()
        self.amps = amps
        self.a = a
        self.b = b

    def apply(self, mat: Matrix):
        mat.add(self.a.index, mat.n, -self.amps)
        mat.add(self.b.index, mat.n, self.amps)


class Circuit:
    def __init__(self):
        self.nodes = []
        self.components = []

    def new_node(self, name) -> Node:
        n = Node(len(self.nodes), name)
        self.nodes.append(n)
        return n

    def new_component(self, comp: Component):
        self.components.append(comp)

    def solve(self):
        mat = Matrix(len(self.nodes))
        for comp in self.components:
            comp.apply(mat)
        return mat


c = Circuit()
v1 = c.new_node("v1")
v2 = c.new_node("v2")
v3 = c.new_node("v3")
gnd = c.new_node("gnd")

c.new_component(Resistor(5, v1, v2))
c.new_component(Resistor(7, v2, v3))
c.new_component(Resistor(10, v2, gnd))
c.new_component(CurrentSource(1, gnd, v1))
c.new_component(CurrentSource(1.5, gnd, v3))

print(c.solve())
