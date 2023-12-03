# Cirkus ⚡

Cirkus is a very minimal electronics circuit simulator which I built for sake of learning electronics. It currently is able to simulate:

- Current sources
- Voltage sources
- Resistors
- Capacitors

The software basically solves a system of differential equations, and components are simply constraints that are added to those equations.

The equations are solved using Newton-Raphson method, and in case there are derivatives in the equations, Backward Euler method is used to convert the differentials to linear equations.