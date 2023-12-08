import random

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

    def numerical_jacobian(self, Vars, delta=1e-6):
        res = []
        for f in range(len(self.funcs)):
            row = []
            for v in range(len(self.funcs)):
                old_val = self.eval(f)
                Vars[v].value += delta
                new_val = self.eval(f)
                Vars[v].value -= delta
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


class Component:
    def __init__(self):
        pass

    def apply(self, solver: Solver):
        raise NotImplemented


class Circuit:
    def __init__(self):
        self.gnd = Var(None, "gnd")
        self.vars = []
        self.components = []

    def new_var(self, name) -> Var:
        n = Var(len(self.vars), name, value=random.random())
        self.vars.append(n)
        return n

    def new_component(self, comp: Component):
        self.components.append(comp)

    def solve(self):
        solver = Solver(len(self.vars))
        for comp in self.components:
            comp.apply(solver)
        return solver
