from circuit import Var, Component, Solver


class Inductor(Component):
    def __init__(self, henries, dt, a: Var, b: Var, i: Var):
        super().__init__()
        self.dt = dt
        self.henries = henries
        self.a = a
        self.b = b
        self.i = i

    def apply(self, solver: Solver):
        solver.add_func(self.a.index, lambda: self.i.value)
        solver.add_func(self.b.index, lambda: -self.i.value)
        solver.add_func(
            self.i.index,
            lambda: (self.i.value - self.i.old_value) / self.dt * self.henries
            - (self.a.value - self.b.value),
        )

        solver.add_deriv(self.a.index, self.i.index, lambda: 1)
        solver.add_deriv(self.b.index, self.i.index, lambda: -1)
        solver.add_deriv(self.i.index, self.i.index, lambda: self.henries / self.dt)
        solver.add_deriv(self.i.index, self.a.index, lambda: -1)
        solver.add_deriv(self.i.index, self.b.index, lambda: 1)
