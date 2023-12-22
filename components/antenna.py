from circuit import Var, Component, Solver
import random


class Antenna(Component):
    def __init__(self, src: Var, dst: Var, gnd: Var, coeff: float, noise: float):
        super().__init__()
        self.coeff = coeff
        self.src = src
        self.dst = dst
        self.gnd = gnd
        self.noise = noise

    def apply(self, solver: Solver):
        solver.add_func(
            self.dst.index,
            lambda: (self.dst.value - self.gnd.value)
            - (self.src.value - self.gnd.value) * self.coeff
            + solver.randomness * self.noise,
        )

        solver.add_deriv(self.dst.index, self.dst.index, lambda: 1)
        solver.add_deriv(self.dst.index, self.gnd.index, lambda: self.coeff - 1)
        solver.add_deriv(self.dst.index, self.src.index, lambda: -self.coeff)
