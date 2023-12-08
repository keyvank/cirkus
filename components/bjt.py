import math
from circuit import Var, Component, Solver


class Bjt(Component):
    def __init__(
        self,
        coeff_in,
        coeff_out,
        beta_r,
        beta_f,
        base: Var,
        collector: Var,
        emitter: Var,
    ):
        super().__init__()
        self.coeff_in = coeff_in
        self.coeff_out = coeff_out
        self.base = base
        self.emitter = emitter
        self.collector = collector
        self.beta_r = beta_r
        self.beta_f = beta_f

    def apply(self, solver: Solver):
        solver.add_func(
            self.collector.index,
            lambda: (
                (
                    math.exp((self.base.value - self.emitter.value) * self.coeff_in)
                    - math.exp((self.base.value - self.collector.value) * self.coeff_in)
                )
                - (1 / self.beta_r)
                * (
                    math.exp((self.base.value - self.collector.value) * self.coeff_in)
                    - 1
                )
            )
            * self.coeff_out,
        )
        solver.add_func(
            self.base.index,
            lambda: (
                (1 / self.beta_f)
                * (math.exp((self.base.value - self.emitter.value) * self.coeff_in) - 1)
                + (1 / self.beta_r)
                * (
                    math.exp((self.base.value - self.collector.value) * self.coeff_in)
                    - 1
                )
            )
            * self.coeff_out,
        )
        solver.add_func(
            self.emitter.index,
            lambda: -(
                (
                    math.exp((self.base.value - self.emitter.value) * self.coeff_in)
                    - math.exp((self.base.value - self.collector.value) * self.coeff_in)
                )
                + (1 / self.beta_f)
                * (math.exp((self.base.value - self.emitter.value) * self.coeff_in) - 1)
            )
            * self.coeff_out,
        )

        solver.add_deriv(
            self.collector.index,
            self.collector.index,
            lambda: math.exp((self.base.value - self.collector.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in
            + math.exp((self.base.value - self.collector.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in
            * (1 / self.beta_r),
        )
        solver.add_deriv(
            self.collector.index,
            self.base.index,
            lambda: math.exp((self.base.value - self.emitter.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in
            - math.exp((self.base.value - self.collector.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in
            - math.exp((self.base.value - self.collector.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in
            * (1 / self.beta_r),
        )
        solver.add_deriv(
            self.collector.index,
            self.emitter.index,
            lambda: -math.exp((self.base.value - self.emitter.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in,
        )

        solver.add_deriv(
            self.base.index,
            self.collector.index,
            lambda: -(1 / self.beta_r)
            * math.exp((self.base.value - self.collector.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in,
        )
        solver.add_deriv(
            self.base.index,
            self.base.index,
            lambda: (1 / self.beta_f)
            * math.exp((self.base.value - self.emitter.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in
            + (1 / self.beta_r)
            * math.exp((self.base.value - self.collector.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in,
        )
        solver.add_deriv(
            self.base.index,
            self.emitter.index,
            lambda: -(1 / self.beta_f)
            * math.exp((self.base.value - self.emitter.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in,
        )

        solver.add_deriv(
            self.emitter.index,
            self.collector.index,
            lambda: -math.exp((self.base.value - self.collector.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in,
        )
        solver.add_deriv(
            self.emitter.index,
            self.base.index,
            lambda: -math.exp((self.base.value - self.emitter.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in
            + math.exp((self.base.value - self.collector.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in
            - (1 / self.beta_f)
            * math.exp((self.base.value - self.emitter.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in,
        )
        solver.add_deriv(
            self.emitter.index,
            self.emitter.index,
            lambda: math.exp((self.base.value - self.emitter.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in
            + (1 / self.beta_f)
            * math.exp((self.base.value - self.emitter.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in,
        )


def test_bjt():
    import numpy

    base = Var(0, "base", 1.8)
    col = Var(1, "col", 1.1)
    em = Var(2, "em", 1.05)
    bjt = Bjt(1 / 0.026, 1e-14, 10, 250, base, col, em)
    solver = Solver(3)
    bjt.apply(solver)
    aa = solver.eval(0)
    bb = solver.eval(1)
    cc = solver.eval(2)
    jac = solver.jacobian([base, col, em])
    num_jac = solver.numerical_jacobian([base, col, em], 1e-10)
    print(numpy.isclose(aa + bb + cc, 0))
    print(numpy.isclose(numpy.array(jac), numpy.array(num_jac)))


if __name__ == "__main__":
    test_bjt()
