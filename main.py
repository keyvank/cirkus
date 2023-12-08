import numpy
import random
from matplotlib import pyplot as plt

from circuit import Circuit, Var, Solver
from components import Resistor, Bjt, VoltageSource, Capacitor

VOLTAGE = 5
R_COLLECTOR = 470
R_BASE = 47000
CAP = 0.000010

c = Circuit()
top = c.new_var()
o1 = c.new_var()
o2 = c.new_var()
b1 = c.new_var()
b2 = c.new_var()
i = c.new_var()

DT = 0.01
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


t = 0

points = []

for _ in range(500):
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
            if numpy.allclose(f_X, 0):
                break
        if not numpy.allclose(f_X, 0):
            raise Exception("Convergence failed!")
    except KeyboardInterrupt as e:
        raise e
    except:
        # Start from another random solution
        for v in c.vars:
            v.value = random.random()
        continue

    print(t, o1.value)
    points.append(o1.value)
    for v in c.vars:
        v.old_value = v.value
    t += DT

plt.plot(points)
plt.show()
