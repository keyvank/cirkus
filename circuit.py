import random
import numpy


class ConvergenceError(Exception):
    pass


class Var:
    def __init__(self, index):
        self.index = index
        self.old_value = 0
        self.value = 0


class Solver:
    def __init__(self, variables, dt) -> None:
        self.variables = variables
        self.funcs = [list() for _ in range(len(variables))]
        self.derivs = [dict() for _ in range(len(variables))]
        self.dt = dt
        self.t = 0

    def jacobian(self):
        res = []
        for f in range(len(self.funcs)):
            row = []
            for v in range(len(self.funcs)):
                row.append(self.eval_deriv(f, v))
            res.append(row)
        return res

    def numerical_jacobian(self, delta=1e-6):
        res = []
        for f in range(len(self.funcs)):
            row = []
            for v in range(len(self.funcs)):
                old_val = self.eval(f)
                self.variables[v].value += delta
                new_val = self.eval(f)
                self.variables[v].value -= delta
                row.append((new_val - old_val) / delta)
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

    def is_solved(self):
        for i in range(len(self.funcs)):
            if not numpy.allclose(self.eval(i), 0):
                return False
        return True

    def step(self, max_iters=1000, max_tries=100, alpha=1):
        solved = False
        for _ in range(max_tries):
            try:
                iters = 0
                while not solved:
                    x = [v.value for v in self.variables]
                    f_x = [self.eval(v.index) for v in self.variables]
                    f_prime_x = self.jacobian()
                    f_prime_x_inv = numpy.linalg.inv(f_prime_x)
                    x = x - alpha * numpy.dot(f_prime_x_inv, f_x)
                    for v in self.variables:
                        v.value = x[v.index]
                    solved = self.is_solved()
                    if iters >= max_iters:
                        raise ConvergenceError
                    iters += 1
            except (OverflowError, ConvergenceError, numpy.linalg.LinAlgError):
                # Start from another random solution
                for v in self.variables:
                    v.value = random.random()
            if solved:
                for v in self.variables:
                    v.old_value = v.value
                self.t += self.dt
                return
        raise ConvergenceError


class Component:
    def __init__(self):
        pass

    def apply(self, solver: Solver):
        raise NotImplemented


class Circuit:
    def __init__(self):
        self.gnd = Var(None)
        self.vars = []
        self.components = []

    def new_var(self) -> Var:
        n = Var(len(self.vars))
        self.vars.append(n)
        return n

    def new_component(self, comp: Component):
        self.components.append(comp)

    def solver(self, dt) -> Solver:
        solver = Solver(self.vars, dt)
        for comp in self.components:
            comp.apply(solver)
        return solver
