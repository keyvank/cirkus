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

        math.exp(
            (self.base.value - self.emitter.value) * self.coeff_in
        ) * self.coeff_out * self.coeff_in

        solver.add_func(
            self.emitter.index,
            lambda: -(
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
            self.collector.index,
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
            self.base.index,
            lambda: (
                (
                    math.exp((self.base.value - self.emitter.value) * self.coeff_in)
                    - math.exp((self.base.value - self.collector.value) * self.coeff_in)
                )
                - (1 / self.beta_f)
                * (math.exp((self.base.value - self.emitter.value) * self.coeff_in) - 1)
            )
            * self.coeff_out,
        )

        solver.add_deriv(
            self.emitter.index,
            self.emitter.index,
            lambda: math.exp((self.base.value - self.emitter.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in,
        )
        solver.add_deriv(
            self.emitter.index,
            self.collector.index,
            lambda: -math.exp((self.base.value - self.collector.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in
            - math.exp((self.base.value - self.collector.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in
            * (1 / self.beta_r),
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
            - math.exp((self.base.value - self.collector.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in
            * (1 / self.beta_r),
        )

        solver.add_deriv(
            self.collector.index,
            self.emitter.index,
            lambda: -(1 / self.beta_f)
            * math.exp((self.base.value - self.emitter.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in,
        )
        solver.add_deriv(
            self.collector.index,
            self.collector.index,
            lambda: -(1 / self.beta_r)
            * math.exp((self.base.value - self.collector.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in,
        )
        solver.add_deriv(
            self.collector.index,
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
            lambda: -math.exp((self.base.value - self.emitter.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in
            + (1 / self.beta_f)
            * math.exp((self.base.value - self.emitter.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in,
        )
        solver.add_deriv(
            self.base.index,
            self.collector.index,
            lambda: math.exp((self.base.value - self.collector.value) * self.coeff_in)
            * self.coeff_out
            * self.coeff_in,
        )
        solver.add_deriv(
            self.base.index,
            self.base.index,
            lambda: math.exp((self.base.value - self.emitter.value) * self.coeff_in)
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
