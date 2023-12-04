import math
from circuit import Var, Component, Solver


class Diode(Component):
    def __init__(self, coeff_in, coeff_out, a: Var, b: Var):
        super().__init__()
        self.coeff_in = coeff_in
        self.coeff_out = coeff_out
        self.a = a
        self.b = b

    def apply(self, solver: Solver):
        solver.add_func(
            self.a.index,
            lambda: (math.exp((self.a.value - self.b.value) * self.coeff_in) - 1)
            * self.coeff_out,
        )
        solver.add_func(
            self.b.index,
            lambda: -(math.exp((self.a.value - self.b.value) * self.coeff_in) - 1)
            * self.coeff_out,
        )

        solver.add_deriv(
            self.a.index,
            self.a.index,
            lambda: math.exp((self.a.value - self.b.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in,
        )
        solver.add_deriv(
            self.a.index,
            self.b.index,
            lambda: -math.exp((self.a.value - self.b.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in,
        )
        solver.add_deriv(
            self.b.index,
            self.a.index,
            lambda: -math.exp((self.a.value - self.b.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in,
        )
        solver.add_deriv(
            self.b.index,
            self.b.index,
            lambda: math.exp((self.a.value - self.b.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in,
        )
