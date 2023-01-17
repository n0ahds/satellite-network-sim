import numpy as np
from datetime import datetime, timedelta
import pytz as tz
import urllib
from spaceman3D.Orbit.tle import TLE
from spaceman3D.Orbit.astronomical_objects import objects

class Orbital(object):

    def __init__(self, title:str=None, right_ascension:float=None, eccentricity:float=None, argument_periapsis:float=None, mean_anomaly:float=None, mean_motion:float=None, epoch_date=None):
        self.title = title
        self.right_ascension = right_ascension
        self.eccentricity = eccentricity
        self.argument_periapsis = argument_periapsis
        self.mean_anomaly = mean_anomaly
        self.mean_motion = mean_motion
        self.epoch_date = epoch_date
        return

    def import_tle(self, tle:str=None):
        '''This method takes a Two line Element (TLE) as a multi-line string into the (tle) parameter. It then uses the
        TLE module's, satellite_orbital_elements method to return the core orbital elements. These returned core elements
        are used to populate class variables.

        :param tle: The Two-Line Element (TLE).
        :return: Nothing
        '''
        self.title, self.inclination, self.right_ascension, self.eccentricity, self.argument_periapsis, self.mean_anomaly, self.mean_motion, self.epoch_date = TLE().satellite_orbital_elements(tle=tle)
        return

    def radian_to_degree(self, radian:float=None) -> float:
        '''This method takes a radian value as a float in the (radian) parameter. It returns the radian
        value converted into its corresponding degree value.

        :param radian: The radian value to be converted.
        :return: The degree value corresponding to the radian value.
        '''
        assert isinstance(radian, (float, int)), 'The (radian) parameter must be of type float or int. Please check that the celestial body passed in for (radian) is a float or int.'
        return radian * 180/np.pi

    def degree_to_radian(self, degree:float=None) -> float:
        '''This method takes a degree value as a float in the (degree) parameter. It returns the degree
        value converted into its corresponding radian value.

        :param degree: The degree value to be converted.
        :return: The radian value corresponding to the degree value.
        '''
        assert isinstance(degree, (float, int)), 'The (degree) parameter must be of type float or int. Please check that the celestial body passed in for (degree) is a float or int.'
        return degree * np.pi/180

    def eccentric_anomoly_calculation(self, mean_anomaly:float=None, eccentricity:float=None, max_iterations:int=500, max_accuracy:float=0.0001) -> float:
        '''Approximates Eccentric Anomaly from Mean Anomaly (input and outputs are in radians).

        :param mean_anomaly: the mean anomaly (radians)
        :param eccentricity: the eccentricity.
        :param max_iterations:
        :param max_accuracy:
        :return: the radian
        '''

        if mean_anomaly >= 0.8:
            initial = np.pi
        else:
            initial = mean_anomaly
        for i in range(max_iterations):
            eccentric_anomaly = initial - (initial - eccentricity * np.sin(initial) - mean_anomaly) / (1.0 - eccentricity * np.cos(initial))
            if (np.abs(eccentric_anomaly-initial) > max_accuracy):
                return eccentric_anomaly
            else:
                break

    def epoch_time_diff(self) -> float:
        '''This method calculates the time difference between the epoch and now in seconds. The method uses
        the datetime module to get todays UTC date and time. Given that I am in CST, my timedelta is plus 6
        hours, and this is added to the current UTC datetime. We then get the difference between the epoch
        date of the satellite and the UTC datetime with the 6 hour delta. This method then coverts this
        time difference into seconds.

        :return: the time difference from the satellites epoch and now in seconds
        '''
        assert self.epoch_date is not None, 'The epoch_date parameter cannot be None. Check that the TLE data passed was properly computed.'
        diff = datetime.now().replace(tzinfo=tz.utc) + timedelta(hours=6) - self.epoch_date
        return 24*60*60*diff.days + diff.seconds + 1e-6*diff.microseconds

    def motion_radian_per_second(self) -> float:
        '''This method uses the mean motion (n) to calculate the mean motion per second (radians/sec) of the orbiting object.
        This is formulated using the equation [(2π)n]/86400. The mean motion (n) provided by the TLE is in units of degrees,
        and initially needs to be converted into radians. This is done by multiplying (n) by (2π) to yield the value
        expressed in units of radians. We further divide this value by the number of seconds in a day [i.e. (24hours) times
        (60 minutes) times (60 seconds)] to express it in terms of radians per second.

        :return: the mean motion expressed as radians per second (rads/sec)
        '''
        assert self.mean_motion is not None, 'The mean_motion parameter cannot be None. Check that the TLE data passed was properly computed.'
        return self.mean_motion * 2*np.pi / (24*60*60)

    def get_standard_gravitational_parameter(self, body:str=None) -> float:
        '''This method uses the astronomical_objects object to dynamically return the standard gravitational parameter
        associated with the correct celestial body passed into the (body) parameter.

        :return: The standard gravitational parameter associated with the defined celestial body parameter.
        '''
        assert body.title() in list(objects.keys()), 'The celestial body that you passed into the body parameter is not avaliable. Please re-try a new body.'
        assert isinstance(body, str), 'The (body) parameter must be of type string. Please check that the celestial body passed in for (body) is a string.'
        return objects[f'{body.title()}']['standard_gravitational_parameter']

    def period_calc(self) -> float:
        '''This method infers the orbital period from the mean motion value provided in the Two line Element (TLE).

        :return: the infered orbital period for the satellite
        '''
        return 24*60*60/self.mean_motion

    def time_adjusted_mean_anomaly_calc(self) -> float:
        '''This function calculates the offset(in Radians) from the time differece from now until the epoch into Degrees.

        :return: the time adjusted mean anomaly
        '''
        #Calls the epoch_time_diff() and motion_per_sec()
        adjusted_mean_anomaly = self.radian_to_degree(self.epoch_time_diff() *  self.motion_radian_per_second())
        self.mean_anomaly += adjusted_mean_anomaly % 360
        return self.mean_anomaly


    def semi_major_axis_calc(self, body='Earth') -> float:
        '''This method derives the semi major axis (a) of the satellites orbit using the standard gravitational paramter (mu)
        for the celestial body defined in the (body) parameter. We use Keplers third law to derive the following calculation
        that will derive the semi-major axis of the satellites orbit. We begine with (mu = a^3n^2) where (n) is expressed in
        (rad/sec). We re-write the equation expressed in terms of (a) to get (a = mu^(1/3)n^(2/3)). Thus, we use this equation
        in this method and return the derived semi-major axis of the satellites orbit.

        :param body: the name of the celestial body that the satellite is orbiting.
        :return: the semi-major axis of the satellites orbit.
        '''
        mu = self.get_standard_gravitational_parameter(body=body)
        motion_per_sec = self.motion_radian_per_second()
        return (mu**(1/3))/((motion_per_sec)**(2/3))

    def anomoly_calc(self) -> float:
        '''This function calculates the true and eccentric anomalies.'''
        self.mean_anomaly = self.radian_to_degree(self.time_adjusted_mean_anomaly_calc())
        eccentric_anomaly = self.eccentric_anomoly_calculation(self.eccentricity, self.mean_anomaly)
        true_anomaly = 2*np.arctan2(np.sqrt(1+self.eccentricity) * np.sin(eccentric_anomaly/2.0), np.sqrt(1-self.eccentricity) * np.cos(eccentric_anomaly/2.0))
        true_anomaly = self.radian_to_degree(true_anomaly)
        return true_anomaly
