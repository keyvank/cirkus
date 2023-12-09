# Cirkus ⚡

Cirkus is a very minimal electronics circuit simulator which I built for sake of learning electronics. It currently is able to simulate:

- Current sources
- Voltage sources
- Resistors
- Capacitors
- Inductors
- Diodes
- BJT Transistors

The software basically solves a system of differential equations, and components are simply constraints that are added to those equations.

The equations are solved using Newton-Raphson method, and in case there are derivatives in the equations, Backward Euler method is used to convert the differentials to linear equations.

Cirkus has been able to successfully simulate an Astable Multivibrator circuit!

![Astable Multivibrator](https://github.com/keyvank/cirkus/assets/4275654/9504e781-4687-489c-94cf-bc53c7e1994c)

Or a RLC circuit!

![RLC](https://github.com/keyvank/cirkus/assets/4275654/ddbd5bf4-3f5b-45d3-867a-a56213a77df5)
