""" PROJECT : Satellite Network Simulation

    FILENAME : entities.py

    DESCRIPTION :
        Simulate a network of satellite nodes to compare performance 
        compared to regular ground nodes.

    FUNCTIONS :
        @dataclass.LEOSatellite
        @dataclass.MEOSatellite
        @dataclass.GroundStation
        @dataclass.Congestion

    NOTES :
        - ...

    AUTHOR(S) : Noah Da Silva    START DATE : 2022.11.26 (YYYY.MM.DD)

    CHANGES :
        - ...

    VERSION     DATE        WHO             DETAILS
    0.1.0       2022.11.26  Noah            Creation of project.
    0.2.0       2023.01.09  Noah            Basic simulation of LEO satellite constellation.
    0.2.1       2023.01.19  Noah            Advanced simulation of LEO satellite constellation.
    0.2.2       2023.01.21  Noah/Ranul      Added some distortion to LEO satellite orbit to better represent Mercator Projection.
    0.3.0       2023.01.22  Noah            Added path from ground station to nearest satellite and shortest path algorithm.
    0.3.1       2023.01.22  Noah            Allows to run multiple endpoint (ground station) pairs at once (not recommended).
    0.4.0       2023.03.17  Noah            Added MEO satellite constellation into routing calculations.
    0.5.0       2023.03.22  Noah            Added load-balancing in form of a dynamic heatmap.
    1.0.0       2023.04.07  Noah            Rewrote the program for efficiency and better dynamic adjustments.
"""

from dataclasses import dataclass, field

import settings


@dataclass
class LEOSatellite:
    """ A dataclass representing a Low Earth Orbit (LEO) satellite.

        Attributes:
            x (float): The x-coordinate of the satellite. Defaults to 0.
            y (float): The y-coordinate of the satellite. Defaults to 0.
            z (int): The z-coordinate of the satellite. Defaults to settings.LEO_ORBIT_HEIGHT.
            delay (float): The delay of the satellite. Defaults to 0.
            phase (float): The phase of the satellite. Defaults to 0.
            frequency (float): The frequency of the satellite. Defaults to settings.LEO_FREQUENCY.
            speed (float): The speed of the satellite. Defaults to settings.LEO_SPEED.
            colour (tuple): The colour of the satellite. Defaults to settings.LEO_INACTIVE_COLOUR.
            width (float): The width of the satellite. Defaults to settings.LEO_WIDTH.`
    """
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
    """ A dataclass representing a Medium Earth Orbit (MEO) satellite.

        Attributes:
            x (float): The x-coordinate of the satellite. Defaults to 0.
            y (float): The y-coordinate of the satellite. Defaults to 0.
            z (int): The z-coordinate of the satellite. Defaults to settings.MEO_ORBIT_HEIGHT.
            delay (float): The delay of the satellite. Defaults to 0.
            phase (float): The phase of the satellite. Defaults to 0.
            frequency (float): The frequency of the satellite. Defaults to settings.MEO_FREQUENCY.
            speed (float): The speed of the satellite. Defaults to settings.MEO_SPEED.
            colour (tuple): The colour of the satellite. Defaults to settings.MEO_INACTIVE_COLOUR.
            width (float): The width of the satellite. Defaults to settings.MEO_WIDTH.
    """
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
    """ A dataclass representing a ground station.

        Attributes:
            x (float): The x-coordinate of the ground station. Defaults to 0.
            y (float): The y-coordinate of the ground station. Defaults to 0.
            z (int): The z-coordinate of the ground station. Defaults to 0.
            colour (tuple): The colour of the ground station. Defaults to settings.GROUND_STATION_COLOUR.
            width (float): The width of the ground station. Defaults to settings.GROUND_STATION_WIDTH.
    """
    x: float = 0
    y: float = 0
    z: int = field(init=False, default=0)
    colour: tuple = field(init=False, default=settings.GROUND_STATION_COLOUR)
    width: float = field(default=settings.GROUND_STATION_WIDTH)


@dataclass
class Congestion:
    """ A dataclass representing congestion.

        Attributes:
            cell_size (int): The size of the cell. Defaults to 0.
            column_num (int): The number of columns. Defaults to 0.
            row_num (int): The number of rows. Defaults to 0.
            grid_density (int): The density of the grid. Defaults to settings.CONGESTION_GRID_DENSITY.
            congestion_map (dict): The congestion map. Defaults to an empty dictionary.
    """
    cell_size: int = 0
    column_num: int = 0
    row_num: int = 0
    grid_density: int = field(init=False, default=settings.CONGESTION_GRID_DENSITY)
    congestion_map: dict = field(init=False, default_factory=lambda:{})