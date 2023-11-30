def f(new_vars: dict, old_vars: dict, dt: float):
    pass

class Variable:
    def __init__(self):
        pass


class Solver:
    def __init__(self):
        self.vars = {}
        self.equations = []
    
    def new_var(self, name):
        v = Variable()
        self.vars[name] = v
        return v

def resistor(ohms, a: str, b: str):
    def f(vars: dict):
        return 0
    return f

def current_source(amps, a: str, b: str):
    def f(vars: dict):
        return 0
    return f

solver = Solver()
solver.equations.append(resistor(5, 'v1', 'v2'))
solver.equations.append(resistor(7, 'v2', 'v3'))
solver.equations.append(resistor(10, 'v2', 'gnd'))
solver.equations.append(current_source(1, 'gnd', 'v1'))
solver.equations.append(current_source(1.5, 'gnd', 'v3'))