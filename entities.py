""" PROJECT : Satellite Network Simulation

    FILENAME : entities.py

    DESCRIPTION :
        Simulate a network of satellite nodes to compare performance 
        compared to regular ground nodes.

    FUNCTIONS :
        dataclass().LEOSatellite
        dataclass().MEOSatellite
        dataclass().GroundStation

    NOTES :
        - ...

    AUTHOR(S) : Noah Da Silva    START DATE : 2022.11.26 (YYYY.MM.DD)

    CHANGES :
        - ...

    VERSION     DATE        WHO             DETAILS
    0.0.1a      2022.11.26  Noah            Creation of project.
    0.0.2a      2023.01.09  Noah            Basic simulation of LEO satellite constellation.
    0.0.2b      2023.01.19  Noah            Advanced simulation of LEO satellite constellation.
    0.0.2c      2023.01.21  Noah/Ranul      Added distortion to LEO satellite orbit to better represent Mercator Projection.
    0.1.0       2023.01.22  Noah            Added path from ground station to nearest satellite and shortest path algorithm.
    0.1.1       2023.01.22  Noah            Allows to run multiple endpoint pairs at once (not recommended).
    0.2.0       2023.03.17  Noah            Added MEO satellite constellation into routing calculations.
    0.3.0       2023.03.22  Noah            Added load-balancing in form of a dynamic heatmap.
    0.4.0       2023.04.07  Noah            Rewrote the program for efficiency and dynamic adjustments.
"""

from dataclasses import dataclass, field

import settings


@dataclass
class LEOSatellite:
    "Satellite following a Low-Earth orbit."
    x: float = 0
    y: float = 0
    z: int = field(init=False, default=settings.LEO_ORBIT_HEIGHT)
    delay: float = 0
    phase: float = 0
    frequency: float = field(init=False, default=settings.LEO_FREQUENCY)
    speed: float = field(init=False, default=settings.LEO_SPEED)
    colour: tuple = field(init=False, default=settings.LEO_INACTIVE_COLOUR)
    width: float = field(init=False, default=settings.LEO_WIDTH)


@dataclass
class MEOSatellite:
    "Satellite following a Middle-Earth orbit."
    x: float = 0
    y: float = 0
    z: int = field(init=False, default=settings.MEO_ORBIT_HEIGHT)
    delay: float = 0
    phase: float = 0
    frequency: float = field(init=False, default=settings.MEO_FREQUENCY)
    speed: float = field(init=False, default=settings.MEO_SPEED)
    colour: tuple = field(init=False, default=settings.MEO_INACTIVE_COLOUR)
    width: float = field(init=False, default=settings.MEO_WIDTH)


@dataclass
class GroundStation:
    "Ground station connecting to LEO satellites."
    x: float = 0
    y: float = 0
    z: int = field(init=False, default=0)
    colour: tuple = field(init=False, default=settings.GROUND_STATION_COLOUR)
    width: float = field(default=settings.GROUND_STATION_WIDTH)


@dataclass
class Congestion:
    cell_size: int = 0
    column_num: int = 0
    row_num: int = 0
    grid_density: int = field(init=False, default=settings.CONGESTION_GRID_DENSITY)
    congestion_map: dict = field(init=False, default_factory=lambda:{})