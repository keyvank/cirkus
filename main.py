from circuit import Circuit
from components import Resistor, Bjt, VoltageSource, Capacitor

VOLTAGE = 1
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

vol = VoltageSource(VOLTAGE, c.gnd, top, i)
c.new_component(vol)
c.new_component(Resistor(R_COLLECTOR, top, o1))
c.new_component(Resistor(R_COLLECTOR, top, o2))
c.new_component(Resistor(R_BASE, top, b1))
c.new_component(Resistor(R_BASE, top, b2))
c.new_component(Capacitor(CAP, o1, b2))
c.new_component(Capacitor(CAP, o2, b1))
c.new_component(Bjt(1 / 0.026, 1e-14, 10, 250, b1, o1, c.gnd))
c.new_component(Bjt(1 / 0.026, 1e-14, 10, 250, b2, o2, c.gnd))

solver = c.solve()

import numpy

for _ in range(100000):
    for _ in range(1000):
        X_prime = solver.jacobian(c.vars)
        X_prime_inv = numpy.linalg.inv(X_prime)
        X = [v.value for v in c.vars]
        f_X = [solver.eval(v.index) for v in c.vars]
        old_x = X
        X = X - numpy.dot(X_prime_inv, f_X)
        for v in c.vars:
            v.value = X[v.index]
    if not numpy.allclose(old_x, X):
        raise Exception("Convergence failed!")
    print(o1.value, o2.value)
    # vol.volts += 0.1
    for v in c.vars:
        v.old_value = v.value
