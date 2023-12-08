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

solver = c.solver()

t = 0
duration = 3  # Seconds

points = []

while t < duration:
    solver.step()
    print(t, o1.value)
    points.append(o1.value)
    t += DT

plt.plot(points)
plt.show()
