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

    t = Var(None)

    c = Circuit()
    top = c.new_var()
    o1 = c.new_var()
    o2 = c.new_var()
    b1 = c.new_var()
    b2 = c.new_var()
    i = c.new_var()

    c.new_component(VoltageSource(VOLTAGE, c.gnd, top, i, t, 0))
    c.new_component(Resistor(R_COLLECTOR, top, o1))
    c.new_component(Resistor(R_COLLECTOR, top, o2))
    c.new_component(Resistor(R_BASE, top, b1))
    c.new_component(Resistor(R_BASE, top, b2))
    c.new_component(Capacitor(CAP, DT, o1, b2))
    c.new_component(Capacitor(CAP, DT, o2, b1))
    c.new_component(Bjt(1 / 0.026, 1e-14, 10, 250, b1, o1, c.gnd))
    c.new_component(Bjt(1 / 0.026, 1e-14, 10, 250, b2, o2, c.gnd))

    solver = c.solver()

    duration = 3  # Seconds

    points = []

    while t.value < duration:
        solver.step()
        print(t.value, o1.value)
        points.append(o1.value)
        t.value += DT

    plt.plot(points)
    plt.show()


def rlc():
    DT = 0.001
    VOLTAGE = 5
    R = 0.5
    L = 1
    CAP = 0.1

    t = Var(None)

    c = Circuit()
    v1 = c.new_var()
    v2 = c.new_var()
    i_inductor = c.new_var()

    c.new_component(Capacitor(CAP, DT, c.gnd, v1))
    c.new_component(Resistor(R, v1, v2))
    c.new_component(Inductor(L, DT, v2, c.gnd, i_inductor))

    v1.old_value = VOLTAGE

    solver = c.solver()

    duration = 10  # Seconds

    points = []

    while t.value < duration:
        solver.step()
        print(t.value, i_inductor.value)
        points.append(i_inductor.value)
        t.value += DT

    plt.plot(points)
    plt.show()


def resonance():
    import math

    DT = 0.0001
    VOLTAGE = 5
    C = 31.7 * 1e-6
    L = 500 * 1e-3
    R = 250

    t = Var(None)

    c = Circuit()
    v1 = c.new_var()
    v2 = c.new_var()
    i_vss = c.new_var()
    i_l = c.new_var()

    resonance_freq = 1 / (2 * math.pi * math.sqrt(L * C))

    c.new_component(VoltageSource(VOLTAGE, c.gnd, v1, i_vss, t, resonance_freq))
    c.new_component(Resistor(R, v1, v2))
    c.new_component(Capacitor(C, DT, v2, c.gnd))
    c.new_component(Inductor(L, DT, v2, c.gnd, i_l))

    solver = c.solver()

    duration = 2  # Seconds

    points = []

    while t.value < duration:
        solver.step()
        print(t.value, v2.value)
        points.append(v2.value)
        t.value += DT

    plt.plot(points)
    plt.show()


rlc()
