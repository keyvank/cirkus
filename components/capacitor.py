from circuit import Var, Component, Solver


class Capacitor(Component):
    def __init__(self, farads, a: Var, b: Var):
        super().__init__()
        self.farads = farads
        self.a = a
        self.b = b

    def apply(self, solver: Solver):
        solver.add_func(
            self.a.index,
            lambda: (
                (self.a.value - self.b.value) - (self.a.old_value - self.b.old_value)
            )
            / solver.dt
            * self.farads,
        )
        solver.add_func(
            self.b.index,
            lambda: -(
                (self.a.value - self.b.value) - (self.a.old_value - self.b.old_value)
            )
            / solver.dt
            * self.farads,
        )

        solver.add_deriv(self.a.index, self.a.index, lambda: self.farads / solver.dt)
        solver.add_deriv(self.a.index, self.b.index, lambda: -self.farads / solver.dt)
        solver.add_deriv(self.b.index, self.a.index, lambda: -self.farads / solver.dt)
        solver.add_deriv(self.b.index, self.b.index, lambda: self.farads / solver.dt)
