import numpy
import random
from matplotlib import pyplot as plt

from circuit import Circuit, Var, Solver
from components import Resistor, Bjt, VoltageSource, Capacitor, Inductor


def astable_multivib():
    DT = 0.01
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


def rlc():
    DT = 0.001
    VOLTAGE = 5
    R = 0.5
    L = 1
    CAP = 0.1

    c = Circuit()
    v1 = c.new_var()
    v2 = c.new_var()
    i_inductor = c.new_var()

    c.new_component(Capacitor(CAP, DT, c.gnd, v1))
    c.new_component(Resistor(R, v1, v2))
    c.new_component(Inductor(L, DT, v2, c.gnd, i_inductor))

    v1.old_value = VOLTAGE

    solver = c.solver()

    t = 0
    duration = 10  # Seconds

    points = []

    while t < duration:
        solver.step()
        print(t, i_inductor.value)
        points.append(i_inductor.value)
        t += DT

    plt.plot(points)
    plt.show()


rlc()
