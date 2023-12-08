from circuit import Var, Component, Solver


class Capacitor(Component):
    def __init__(self, farads, dt, a: Var, b: Var):
        super().__init__()
        self.dt = dt
        self.farads = farads
        self.a = a
        self.b = b

    def apply(self, solver: Solver):
        solver.add_func(
            self.a.index,
            lambda: (
                (self.a.value - self.b.value) - (self.a.old_value - self.b.old_value)
            )
            / self.dt
            * self.farads,
        )
        solver.add_func(
            self.b.index,
            lambda: -(
                (self.a.value - self.b.value) - (self.a.old_value - self.b.old_value)
            )
            / self.dt
            * self.farads,
        )

        solver.add_deriv(self.a.index, self.a.index, lambda: self.farads / self.dt)
        solver.add_deriv(self.a.index, self.b.index, lambda: -self.farads / self.dt)
        solver.add_deriv(self.b.index, self.a.index, lambda: -self.farads / self.dt)
        solver.add_deriv(self.b.index, self.b.index, lambda: self.farads / self.dt)
