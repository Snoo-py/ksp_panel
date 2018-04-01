# ksp_panel

Ksp panel provide a schematic view of your orbit and orbital parameter.
Ksp panel using the KRPC mod to communicate with kerbal space program.

## Dependencies
- [krpc](https://krpc.github.io/krpc/python/client.html#installing-the-library)
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/download5)
- numpy

# Example
- To run:
```
./ksp_panel.py -H 1.2.3.4
```

![orbital mfd](https://github.com/Snoo-py/ksp_panel/blob/master/doc/orbital_mfd_legend.jpg?raw=true)

- Pe: Periapsis of your orbit, in meters, from the center of mass of the body being orbited.
- Ap: Apoapsis of your orbit, in meters, from the center of mass of the body being orbited.
- Ecc: Eccentricity of your orbit.
- PeT: Time until your vessel reach periapsis, in seconds.
- ApT: Time until your vessel reach apoapsis, in seconds.
- Vel: Current orbital speed in meters per second.
- Inc: Inclination of the orbit, in degree.
- LAN: Longitude of the ascending node, in degree.
- LPe: Longitude of the periapsis, in degree.
