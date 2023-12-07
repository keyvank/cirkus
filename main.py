from circuit import Circuit
from components import Resistor, Bjt, VoltageSource


c = Circuit()
v1 = c.new_var("v1")
v2 = c.new_var("v2")
v3 = c.new_var("v3")
i = c.new_var("i")

from components.bjt import Bjt

c.new_component(VoltageSource(3, c.gnd, v1, i))
c.new_component(Resistor(100, v1, v2))
c.new_component(Resistor(100, v1, v3))
c.new_component(Bjt(1 / 0.026, 1e-14, 10, 250, v2, v3, c.gnd))


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
    print(v1.value, v2.value, v3.value, i.value)
    for v in c.vars:
        v.old_value = v.value
