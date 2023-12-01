from matrix import Matrix


class Solver:
    def __init__(self, num_funcs) -> None:
        self.funcs = [list() for _ in range(num_funcs)]

    def jacobian(self, nodes):
        h = 1e-6
        res = []
        for f in range(len(self.funcs)):
            row = []
            for v in range(len(self.funcs)):
                old = self.eval(f)
                nodes[v].value += h
                new = self.eval(f)
                nodes[v].value -= h
                row.append((new - old) / h)
            res.append(row)
        return res

    def add_func(self, ind, f):
        if ind is not None:
            self.funcs[ind].append(f)

    def eval(self, ind):
        res = 0
        for f in self.funcs[ind]:
            res += f()
        return res


class Node:
    def __init__(self, index, name, value=0):
        self.index = index
        self.name = name
        self.value = value


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

    def apply(self, solver: Solver):
        solver.add_func(self.a.index, lambda: (self.a.value - self.b.value) / self.ohms)
        solver.add_func(self.b.index, lambda: (self.b.value - self.a.value) / self.ohms)


class CurrentSource(Component):
    def __init__(self, amps, a: Node, b: Node):
        super().__init__()
        self.amps = amps
        self.a = a
        self.b = b

    def apply(self, solver: Matrix):
        solver.add_func(self.a.index, lambda: self.amps)
        solver.add_func(self.b.index, lambda: -self.amps)


class Circuit:
    def __init__(self):
        self.gnd = Node(None, 'gnd')
        self.nodes = []
        self.components = []

    def new_node(self, name) -> Node:
        n = Node(len(self.nodes), name)
        self.nodes.append(n)
        return n

    def new_component(self, comp: Component):
        self.components.append(comp)

    def solve(self):
        solver = Solver(len(self.nodes))
        for comp in self.components:
            comp.apply(solver)
        return solver


c = Circuit()
v1 = c.new_node("v1")
v2 = c.new_node("v2")
v3 = c.new_node("v3")

c.new_component(Resistor(5, v1, v2))
c.new_component(Resistor(7, v2, v3))
c.new_component(Resistor(10, v2, c.gnd))
c.new_component(CurrentSource(1, c.gnd, v1))
c.new_component(CurrentSource(1.5, c.gnd, v3))

solver = c.solve()

import numpy

for _ in range(10):
    X_prime = solver.jacobian([v1, v2, v3])
    X_prime_inv = numpy.linalg.inv(X_prime)
    X = [v1.value, v2.value, v3.value]
    f_X = [solver.eval(0), solver.eval(1), solver.eval(2)]
    X = X - numpy.dot(X_prime_inv, f_X)
    v1.value = X[0]
    v2.value = X[1]
    v3.value = X[2]

print(v1.value)
print(v2.value)
print(v3.value)
