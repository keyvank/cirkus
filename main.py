DT = 0.1

class Var:
    def __init__(self, index, name, value=0):
        self.index = index
        self.name = name
        self.old_value = 0
        self.value = value


class Solver:
    def __init__(self, num_funcs) -> None:
        self.funcs = [list() for _ in range(num_funcs)]
        self.derivs = [dict() for _ in range(num_funcs)]

    def jacobian(self, Vars):
        res = []
        for f in range(len(self.funcs)):
            row = []
            for v in range(len(self.funcs)):
                row.append(self.eval_deriv(f, v))
            res.append(row)
        return res

    def add_func(self, ind, f):
        if ind is not None:
            self.funcs[ind].append(f)

    def add_deriv(self, ind, by_ind, f):
        if ind is not None:
            if by_ind not in self.derivs[ind]:
                self.derivs[ind][by_ind] = []
            self.derivs[ind][by_ind].append(f)

    def eval(self, ind):
        res = 0
        for f in self.funcs[ind]:
            res += f()
        return res

    def eval_deriv(self, ind, by_ind):
        res = 0
        if by_ind in self.derivs[ind]:
            for f in self.derivs[ind][by_ind]:
                res += f()
        return res


class Component:
    def __init__(self):
        pass

    def apply(self, solver: Solver):
        raise NotImplemented


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
            / DT
            * self.farads,
        )
        solver.add_func(
            self.b.index,
            lambda: -(
                (self.a.value - self.b.value) - (self.a.old_value - self.b.old_value)
            )
            / DT
            * self.farads,
        )

        solver.add_deriv(self.a.index, self.a.index, lambda: self.farads / DT)
        solver.add_deriv(self.a.index, self.b.index, lambda: -self.farads / DT)
        solver.add_deriv(self.b.index, self.a.index, lambda: -self.farads / DT)
        solver.add_deriv(self.b.index, self.b.index, lambda: self.farads / DT)


import math


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


class CurrentSource(Component):
    def __init__(self, amps, a: Var, b: Var):
        super().__init__()
        self.amps = amps
        self.a = a
        self.b = b

    def apply(self, solver: Solver):
        solver.add_func(self.a.index, lambda: self.amps)
        solver.add_func(self.b.index, lambda: -self.amps)


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


class Circuit:
    def __init__(self):
        self.gnd = Var(None, "gnd")
        self.vars = []
        self.components = []

    def new_var(self, name) -> Var:
        n = Var(len(self.vars), name, value=1)
        self.vars.append(n)
        return n

    def new_component(self, comp: Component):
        self.components.append(comp)

    def solve(self):
        solver = Solver(len(self.vars))
        for comp in self.components:
            comp.apply(solver)
        return solver


c = Circuit()
v1 = c.new_var("v1")
v2 = c.new_var("v2")
v3 = c.new_var("v3")
i = c.new_var("i")

c.new_component(VoltageSource(10, c.gnd, v1, i))
c.new_component(Diode(1 / 0.026, 1e-14, v1, v2))
c.new_component(Resistor(50, v2, v3))
c.new_component(Capacitor(1, v3, c.gnd))


solver = c.solve()

import numpy

for _ in range(100000):
    for _ in range(1000):
        X_prime = solver.jacobian([v1, v2, v3, i])
        X_prime_inv = numpy.linalg.inv(X_prime)
        X = [v1.value, v2.value, v3.value, i.value]
        f_X = [solver.eval(0), solver.eval(1), solver.eval(2), solver.eval(3)]
        old_x = X
        X = X - numpy.dot(X_prime_inv, f_X)
        v1.value = X[0]
        v2.value = X[1]
        v3.value = X[2]
        i.value = X[3]
    if not numpy.allclose(old_x, X):
        raise Exception("Convergence failed!")
    print(v3.value - c.gnd.value, i.value)
    v1.old_value = v1.value
    v2.old_value = v2.value
    v3.old_value = v3.value
    i.old_value = i.value
