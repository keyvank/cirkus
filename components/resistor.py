from circuit import Var, Component, Solver


class Resistor(Component):
    def __init__(self, ohms, a: Var, b: Var):
        super().__init__()
        self.ohms = ohms
        self.a = a
        self.b = b

    def apply(self, solver: Solver):
        solver.add_func(self.a.index, lambda: (self.a.value - self.b.value) / self.ohms)
        solver.add_func(self.b.index, lambda: (self.b.value - self.a.value) / self.ohms)

        solver.add_deriv(self.a.index, self.a.index, lambda: 1 / self.ohms)
        solver.add_deriv(self.a.index, self.b.index, lambda: -1 / self.ohms)
        solver.add_deriv(self.b.index, self.a.index, lambda: -1 / self.ohms)
        solver.add_deriv(self.b.index, self.b.index, lambda: 1 / self.ohms)
