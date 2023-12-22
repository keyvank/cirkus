import numpy
import random
from matplotlib import pyplot as plt

from circuit import Circuit, Var, Solver
from components import Resistor, Bjt, VoltageSource, Capacitor, Inductor, Antenna, Diode


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

    c.new_component(VoltageSource(VOLTAGE, c.gnd, top, i, 0))
    c.new_component(Resistor(R_COLLECTOR, top, o1))
    c.new_component(Resistor(R_COLLECTOR, top, o2))
    c.new_component(Resistor(R_BASE, top, b1))
    c.new_component(Resistor(R_BASE, top, b2))
    c.new_component(Capacitor(CAP, o1, b2))
    c.new_component(Capacitor(CAP, o2, b1))
    c.new_component(Bjt(1 / 0.026, 1e-14, 10, 250, b1, o1, c.gnd))
    c.new_component(Bjt(1 / 0.026, 1e-14, 10, 250, b2, o2, c.gnd))

    solver = c.solver(DT)

    duration = 3  # Seconds

    points = []

    while solver.t < duration:
        solver.step()
        print(solver.t, o1.value)
        points.append(o1.value)

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

    c.new_component(Capacitor(CAP, c.gnd, v1))
    c.new_component(Resistor(R, v1, v2))
    c.new_component(Inductor(L, v2, c.gnd, i_inductor))

    v1.old_value = VOLTAGE

    solver = c.solver(DT)

    duration = 10  # Seconds

    points = []

    while solver.t < duration:
        solver.step()
        print(solver.t, i_inductor.value)
        points.append(i_inductor.value)

    plt.plot(points)
    plt.show()


def resonance():
    import math

    DT = 0.0001
    VOLTAGE = 5
    C = 31.7 * 1e-6
    L = 500 * 1e-3
    R = 250

    c = Circuit()
    v1 = c.new_var()
    v2 = c.new_var()
    i_vss = c.new_var()
    i_l = c.new_var()

    resonance_freq = 1 / (2 * math.pi * math.sqrt(L * C))

    c.new_component(VoltageSource(VOLTAGE, c.gnd, v1, i_vss, resonance_freq))
    c.new_component(Resistor(R, v1, v2))
    c.new_component(Capacitor(C, v2, c.gnd))
    c.new_component(Inductor(L, v2, c.gnd, i_l))

    solver = c.solver(DT)

    duration = 2  # Seconds

    points = []

    while solver.t < duration:
        solver.step()
        print(solver.t, v2.value)
        points.append(v2.value)

    plt.plot(points)
    plt.show()


def antenna():
    DT = 0.001
    VOLTAGE = 5
    R = 0.0001
    L = 0.1
    CAP = 0.1
    AM_CAP = 0.0001

    c = Circuit()
    v1 = c.new_var()
    v2 = c.new_var()
    i_inductor = c.new_var()

    i_vol = c.new_var()
    v2_2 = c.new_var()
    i_inductor_2 = c.new_var()
    v3 = c.new_var()
    v4 = c.new_var()
    v5 = c.new_var()

    c.new_component(Capacitor(CAP, c.gnd, v1))
    c.new_component(Resistor(R, v1, v2))
    c.new_component(Inductor(L, v2, c.gnd, i_inductor))

    c.new_component(VoltageSource(5, c.gnd, v4, i_vol, 0))
    c.new_component(Capacitor(CAP, v2_2, c.gnd))
    c.new_component(Inductor(L, v2_2, c.gnd, i_inductor_2))
    c.new_component(Diode(1 / 0.026, 1e-14, v2_2, v3))
    c.new_component(Capacitor(AM_CAP, v3, c.gnd))
    c.new_component(Bjt(1 / 0.026, 1e-14, 10, 250, v3, v4, v5))
    c.new_component(Resistor(100, v5, c.gnd))

    c.new_component(Antenna(v1, v2_2, c.gnd, 1, 0))

    solver = c.solver(DT)

    duration = 10  # Seconds

    points = []

    flag_on = False
    flag_off = False

    while solver.t < duration:
        if solver.t > 4 and not flag_on:
            v1.old_value = VOLTAGE
            flag_on = True

        if solver.t > 6 and not flag_off:
            v1.old_value = 0
            i_inductor.old_value = 0
            flag_off = True

        solver.step()
        print(solver.t, i_vol.value)
        points.append(i_vol.value)

    plt.plot(points)
    plt.show()


antenna()
