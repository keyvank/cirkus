from circuit import Circuit, Var, Solver
from components import Resistor, Bjt, VoltageSource, Capacitor


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


test_bjt()
# exit(0)

VOLTAGE = 5
R_COLLECTOR = 470
R_BASE = 47000
CAP = 0.000010

c = Circuit()
top = c.new_var("top")
o1 = c.new_var("o1")
o2 = c.new_var("o2")
b1 = c.new_var("b1")
b2 = c.new_var("b2")
i = c.new_var("i")

from components.bjt import Bjt

DT = 0.05

c.new_component(VoltageSource(VOLTAGE, c.gnd, top, i))
c.new_component(Resistor(R_COLLECTOR, top, o1))
c.new_component(Resistor(R_COLLECTOR, top, o2))
c.new_component(Resistor(R_BASE, top, b1))
c.new_component(Resistor(R_BASE, top, b2))
c.new_component(Capacitor(CAP, DT, o1, b2))
c.new_component(Capacitor(CAP, DT, o2, b1))
c.new_component(Bjt(1 / 0.026, 1e-14, 10, 250, b1, o1, c.gnd))
c.new_component(Bjt(1 / 0.026, 1e-14, 10, 250, b2, o2, c.gnd))

solver = c.solve()

import numpy, random

for _ in range(100000):
    try:
        for _ in range(1000):
            X_prime = solver.jacobian(c.vars)
            X_prime_inv = numpy.linalg.inv(X_prime)
            X = [v.value for v in c.vars]
            f_X = [solver.eval(v.index) for v in c.vars]
            old_x = X
            X = X - numpy.dot(X_prime_inv, f_X)
            for v in c.vars:
                v.value = X[v.index]
        if not numpy.allclose(f_X, 0):
            raise Exception("Convergence failed!")
    except KeyboardInterrupt as e:
        raise e
    except:
        # Start from another random solution
        for v in c.vars:
            v.value = random.random()
        continue

    print(o1.value, o2.value)
    for v in c.vars:
        v.old_value = v.value
