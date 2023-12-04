from circuit import Var, Component, Solver


class VoltageSource(Component):
    def __init__(self, volts, a: Var, b: Var, i: Var):
        super().__init__()
        self.volts = volts
        self.a = a
        self.b = b
        self.i = i

    def apply(self, solver: Solver):
        solver.add_func(self.a.index, lambda: self.i.value)
        solver.add_func(self.b.index, lambda: -self.i.value)
        solver.add_func(self.i.index, lambda: self.b.value - self.a.value - self.volts)

        solver.add_deriv(self.a.index, self.i.index, lambda: 1)
        solver.add_deriv(self.b.index, self.i.index, lambda: -1)
        solver.add_deriv(self.i.index, self.a.index, lambda: -1)
        solver.add_deriv(self.i.index, self.b.index, lambda: 1)
