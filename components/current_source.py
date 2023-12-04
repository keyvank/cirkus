from circuit import Var, Component, Solver


class CurrentSource(Component):
    def __init__(self, amps, a: Var, b: Var):
        super().__init__()
        self.amps = amps
        self.a = a
        self.b = b

    def apply(self, solver: Solver):
        solver.add_func(self.a.index, lambda: self.amps)
        solver.add_func(self.b.index, lambda: -self.amps)
