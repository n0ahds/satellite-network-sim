from datetime import datetime, timedelta
import pytz as tz
import pandas as pd

class TLE(object):

    def __init__(self):
        return

    def parse_tle(self, tle:str=None) -> tuple:
        '''This method takes a Two line Element (TLE) as a multi-line string into the (tle) parameter. It then breaks it down into its
        individual components. The important thing to consider with this method is that it implicitly makes the assumption that
        there is a title associated with the TLE. So only pass in a TLE that contains a title in the first-row.

        Correct TLE Format:

        """ISS (ZARYA)
        1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
        2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537"""

        :param tle: The Two-Line Element (TLE).
        :return: The individual lines from the TLE, and the title of the satellite.
        '''
        assert isinstance(tle, str), 'The (tle) parameter must be of type string. Please check that the Two line Element (TLE) passed in for tle is a Multi-Line String.'
        assert len(tle.split('\n'))==3, 'It looks like you are missing a row in your TLE. There should be three rows of information, with the title being the first row.'

        title, line1, line2 = map(lambda x: x.strip(), tle.split('\n'))
        return title, line1, line2

    def tle_checksum_algortithm(self, line:str=None) -> str:
        '''This method defines an algorithm to calculate the the Modulo-10 checksum for a line within a Two line Element (TLE). The checksum value
        is used to determine validity and certantity of correctness for each line within the TLE. Thus, this method returns the value of the
        Modulo-10 checksum for the TLE line that was passed into it, cast as a string. We will this calculated value to verify the validity of the
        lines in a TLE, by comparing it to the checksum provided with the TLE. The provided value is the last digit, located at the end of each of
        the 2 TLE lines, excluding the title line.

        :param line: The Two line Element (TLE) line to be checked.
        :return: The value of the Modulo-10 Checksum for the defined line, cast as a string.
        '''
        assert isinstance(line, str), 'The (line) parameter must be of type string. Please check that the (line) passed in is a string.'

        line = line.replace('-','1')
        digits = [int(d) for d in line if d.isdigit()]
        mod10_chksum = str(sum(digits[:-1]) % 10)
        return mod10_chksum

    def validation_framework(self, condition1:str=None, condition2:str=None, expected1:str=None, expected2:str=None, dual_condition:bool=True) -> bool:
        '''This method is super useful because it allows us to define a couple of types of conditional tests which are used to check the
        validity of the TLE data. The first and more frequently used type is the dual condition test. We use this to check that both of
        the two conditions match their expected values. The second is a single condition test which checks if a single condition matches the an
        expected value. Regardless, of the number of conditions this method returns True if the conditions are met, and False if they are
        not met.

        :param condition1: This is the first condition that is to be verified.
        :param condition2: This is an optional second condition that is to be verified.
        :param expected1: This is the expected value that the first condition should match.
        :param expected2: This is the second expected value that the second condition should match.
        :param dual_condition: If this is True, then you are testing that two conditions match.
        :return: A boolean value indicating whether the conditions being tested are the same.
        '''
        params = (condition1, expected1)
        for param in params:
            assert isinstance(param, str), f'The ({param}) must be of type string. Please check that the value passed in for ({param}) is a string.'
        assert isinstance(dual_condition, bool), 'The (dual_condition) must be of type bool. Please check that the value passed in for (dual_condition) is a string.'

        if dual_condition == True:
            params = (condition2, expected2)
            for param in params:
                assert isinstance(param, str), f'The ({param}) must be of type string. Please check that the value passed in for ({param}) is a string.'
            if (condition1 == expected1) and (condition2 == expected2):
                return True
            else:
                return False
        else:
            if condition1 == expected1:
                return True
            else:
                return False

    def check_valid_tle(self, tle:str=None) -> bool:
        '''This method takes a Two-Line Element (TLE) and runs through several validation checks of the data contained within it
        to assert the correctness of the TLE. The first check is the confirmation of the line indicators. Each line, excluding the
        title line, have in their first digit, a number representing the whether the line is the first or the second in the TLE.
        This is represented by a 1, and 2 respectively. The Second Check is a confirmation that the satellite number matches between
        the first and second lines. The Third Check, uses the tle_checksum_algortithm to calculate the predicited Modulo-10 checksum
        for each line, and then compares this value with the last digit (i.e. the Modulo-10 checksum) in each line. If all of these
        checks pass, then the the method returns True. If not, the method returns False.

        :param tle: This is a Two-Line Element (TLE) to check.
        :return: A boolean value indicating the validity of the data in the TLE.
        '''

        title, line1, line2 =  self.parse_tle(tle)
        line_index_chk = self.validation_framework(condition1=line1[0], condition2=line2[0],expected1='1',expected2='2')
        sat_number_chk = self.validation_framework(condition1=line1[2:7], expected1=line2[2:7], dual_condition=False)
        checksum_chk = self.validation_framework(condition1=self.tle_checksum_algortithm(line1), condition2=self.tle_checksum_algortithm(line2), expected1=line1[-1], expected2=line2[-1])
        if line_index_chk and sat_number_chk and checksum_chk is True:
            return True
        else:
            return False

    def scientific_notation_conversion(self, element:str=None) -> float:
        '''This method takes in an element in this format (01234-5) as + or (-01234-5) as -, and converts them into
        a float value in e-Notation 1.234e-08. The two specific elements which require this conversion are the BSTAR drag term and
        the second derivative of mean motion. Once the element is converted the method returns the element as a float in e-Notation.

        :param element: a element that needs converted. (Example: 01234-5)
        :return: The element as a float in e-Notation.
        '''
        assert isinstance(element, str), 'The (element) must be of type string. Please check that the value passed in for (element) is a string.'
        assert len(element)==8, 'The length of the (element) must be 8 characters long. Please check that the value passed in for (element) is the correct length.'

        def drop_leading_chars(element:str=None) -> int:
            '''This nested function takes an element as a string and then then returns the length of the string without
            zeros or a negative sign.'''
            i=0
            for char in element:
                if (char=='0') or (char=='-') or (char==' '):
                    i+=1
                    if i < len(element):
                        continue
                    else:
                        return 0
                else:
                    return len(element[i:])
        exp = element[-2:]
        base = element[:-2]
        decimal_places = drop_leading_chars(base)
        multiplier = 0.1 ** decimal_places
        base = multiplier * int(base)
        exponent =  10 ** int(exp)
        return base * exponent

    def decimal_conversion(self, element:str=None) -> float:
        '''This method takes an in an element in this format (001) and adds a leading decimal point (0.001). It then returns
        the element as a float value. In the TLE, the value for the eccentricity is assumed to have a leading decimal value. Thus, this is
        useful when we derive the eccentricty from the TLE. This method works on both negative and non-negative values.

        :param element: An element to have a leading decimal added onto it.
        :return: The element with the leading decimal cast as a float.
        '''
        return float(f'-0.{element[1:]}') if element[0] == '-' else float(f'0.{element}')

    def individual_element(self, tle:str=None, line:int=None, start:int=None, end:int=None, func=None):
        '''This method is used to parse out the relevant individual elements within a Two-Line Element (TLE). The method uses the
        TLE passed into the (tle) parameter, in conjunction with the (line), (start), and (end) parameters to correctly slice out
        an individual element within a TLE . In the event that the individual element needs to be correctly formatted the (func)
        parameter is passed and appropriatly formats the element.

        :param tle: The Two-Line Element (TLE).
        :param line: An integer indicating the line of the TLE that the elment is contained in.
        :param start: The starting position within the specified line for the element.
        :param end: The ending position within the specified line for the element.
        :param func: The function that is used to convert to the element to the proper format.
        :return: The properly formatted TLE.
        '''
        assert self.check_valid_tle(tle) is True, "Your TLE data failed the validity check. Confirm that the data is correct, and try again."
        assert isinstance(line, int), 'The line parameter needs to be of type int. Please check that the value passed is of type int.'
        assert isinstance(start, int), 'The start parameter needs to be of type int. Please check that the value passed is of type int.'
        assert isinstance(end, int), 'The end parameter needs to be of type int. Please check that the value passed is of type int.'

        title, line1, line2 =  self.parse_tle(tle)
        line = line1 if line==1 else line2
        value = func(line[start:end]) if func is not None else line[start:end]
        return value

#################### Parsing the individual TLE components ####################

    def ballistic_coeffecient(self, tle:str=None) -> float:
        '''This method parses and returns the ballistic coeffecient from the Two-Line Element (TLE). This is also called
        the first derivative of mean motion. It is defined as the daily rate of change in the number of revolutions
        that an orbiting object completes each day, divided by 2. This is a "catch all" drag term used in
        the Simplified General Perturbations (SGP4) USSPACECOM predictor. (NASA 1)

        Definition Citation:
        1. “Definition of Two-line Element Set Coordinate System.” SpaceFlight, National Aeronautics and Space Administration,
                23, Sept. 2011, https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html.

        :param tle: The Two-Line Element (TLE).
        :type tle: str
        :return: Ballistic Coeffecient (Revolutions/Day)
        '''
        return self.individual_element(tle,1,33,43,func=float)

    def second_time_derivative_of_mean_motion(self, tle:str=None) -> float:
        '''This method parses and returns the second derivative of mean motion from the Two-Line Element (TLE).
        The second derivative of mean motion is a "second-order" drag term in the SGP4 predictor used to
        model terminal orbit decay. It measures the second time derivative in daily mean motion, divided
        by 6. (NASA 1)

        Definition Citation:
        1. “Definition of Two-line Element Set Coordinate System.” SpaceFlight, National Aeronautics and Space Administration,
                23, Sept. 2011, https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html.

        :param tle: The Two-Line Element (TLE).
        :return: The 2nd Time Derivative of Mean Motion (Revolutions/Day^3)
        '''
        return self.individual_element(tle,1,44,52,func=self.scientific_notation_conversion)

    def bstar_drag_term(self, tle:str=None) -> float:
        '''This method parses and returns the BSTAR drag term from the Two-Line Element (TLE). Also called the
        radiation pressure coefficient, the parameter is another drag term in the SGP4 predictor. (NASA 1)

        Definition Citation:
        1. “Definition of Two-line Element Set Coordinate System.” SpaceFlight, National Aeronautics and Space Administration,
                23, Sept. 2011, https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html.

        :param tle: The Two-Line Element (TLE).
        :return: The B-Star Drag Term (earth radii^-1)
        '''
        return self.individual_element(tle,1,53,61,func=self.scientific_notation_conversion)

    def satellite_number_and_classification(self, tle:str=None) -> int:
        '''This method parses and returns the satellite number from the Two-Line Element (TLE). Similar to
        the International Designator, the satellite number is a naming convention used to catalog satellites by the
        United States Space Command (USSPACECOM). Each geocentric satellite is tracked and denoted by a 5-digit satellite
        number, and is given a classification for each piece of the satellite. (Wikipeda 1)

        Definition Citation:
        1. “Satellite Catalog Number.” Wikipedia,
                7, Feb. 2018, https://en.wikipedia.org/wiki/Satellite_Catalog_Number

        :param tle: The Two-Line Element (TLE).
        :return: The satellites number.
        '''
        return self.individual_element(tle,1,2,7,func=int)

    def classification(self, tle:str=None) -> str:
        '''This method parses and returns the classification type of the satellite from the Two-Line Element (TLE).
        Similar to the International Designator, the satellite number and classification is a naming convention used
        to catalog satellites by the United States Space Command (USSPACECOM). Each geocentric satellite is tracked and
        denoted by a 5-digit satellite number, and is given a classification for each piece of the satellite. (Wikipeda 1)

        Definition Citation:
        1. “Satellite Catalog Number.” Wikipedia,
                7, Feb. 2018, https://en.wikipedia.org/wiki/Satellite_Catalog_Number

        :param tle: The Two-Line Element (TLE).
        :return: The satellites classification. (i.e. U is an Unclassified piece: C is a Classified piece: S is a Secret piece)
        '''
        return self.individual_element(tle,1,7,8,func=str)

    def international_designator_year(self, tle:str=None) -> int:
        '''This method parses and returns the international designator year from the Two-Line Element (TLE). The International
        Designator, also known as the COSPAR designation, or in the U.S as NSSDC ID, is a naming convention for satellites
        parts. It consists of the launch year, a launch number of that year, and a code identifying each of a piece in a
        launch (Wikipedia 1).

        Definition Citation:
        1. “International Designator.” Wikipedia,
                15, May 2018, https://en.wikipedia.org/wiki/International_Designator.

        :param tle: The Two-Line Element (TLE).
        :return: The International Designator Year
        '''
        return self.individual_element(tle,1,9,11,func=int)

    def international_designator_launch_number(self, tle:str=None) -> int:
        '''This method parses and returns the international designator launch number from the Two-Line Element (TLE). The
        International Designator, also known as the COSPAR designation, or in the U.S as NSSDC ID, is a naming convention
        for satellites parts. It consists of the launch year, a 3-digit incrementing launch number of that year and up to
        a code representing the sequential identifier of a piece in a launch (Wikipedia 1).

        Definition Citation:
        1. “International Designator.” Wikipedia,
                15, May 2018, https://en.wikipedia.org/wiki/International_Designator.

        :param tle: The Two-Line Element (TLE).
        :return: The International Designator Launch Number.
        '''
        return self.individual_element(tle,1,11,14,func=int)

    def international_designator_piece_of_launch(self, tle:str=None) -> str:
        '''This method parses and returns the international designator piece of launch from the Two-Line Element (TLE). The
        International Designator, also known as the COSPAR designation, or in the U.S as NSSDC ID, is a naming convention for
        satellites parts. It consists of the launch year, a launch number of that year, and a code identifying each of a piece in a launch
        (Wikipedia 1).

        Definition Citation:
        1. “International Designator.” Wikipedia,
                15, May 2018, https://en.wikipedia.org/wiki/International_Designator.

        :param tle: The Two-Line Element (TLE).
        :return: the international_designator_piece_of_launch element.
        '''
        return self.individual_element(tle,1,14,17,func=str)

    def element_set_number(self, tle:str=None) -> int:
        '''This method parses and returns the element set number from the Two-Line Element (TLE) The element set number is a
        value representing the version of the TLE that the TLE is. Put more simply, the element set number is incremented by
        one with each new version of a TLE for that orbiting object (Wikipedia 1).

        Definition Citation:
        1. “Two-Line Element set.” Wikipedia,
                17, October 2019, https://en.wikipedia.org/wiki/Two-line_element_set.

        :param tle: The Two-Line Element (TLE).
        :return: the Element Set Number.
        '''
        return self.individual_element(tle,1,64,68,func=int)

    def epoch_year(self, tle:str=None, full_year:bool=False) -> int:
        '''This method parses and returns the epoch year from the Two-Line Element (TLE). The TLE provides the epoch year using
        2-digits (i.e. 08) or (i.e. 98). Every century, the year can represent different values. If my code is used in 2070, then
        this is going to need to be updated. But come on, who is even reading this, much less using it?? That said, if the full_year
        parameter is set to True, this method will return the 4-digit year (i.e. 2008 or 1998). The default behavior is to return
        just the 2-digit format.

        :param tle: The Two-Line Element (TLE).
        :return: either the full year (4-digits) or the epoch year (2-digits).
        '''
        assert isinstance(full_year, bool), "The full_year argument must be of type bool. Please check that the value passed is of type bool."

        epoch_year = self.individual_element(tle,1,18,20,func=int)
        if full_year is True:
            epoch_year = 2000 + epoch_year if epoch_year < 70 else 1900 + epoch_year
        return epoch_year

    def epoch(self, tle:str=None) -> float:
        '''This method parses and returns the epoch days from the Two-Line Element (TLE). The epoch is a concept in astronomy
        which is a moment in time, that serves as reference point for some astronomical quantity. This method returns epoch
        denoted in the number of Julian calander days within the epoch year from when this TLE was created.

        :param tle: The Two-Line Element (TLE).
        :return: The epoch (Julian Calander Days)
        '''
        return self.individual_element(tle,1,20,32,func=float)

    def epoch_date(self, tle:str=None):
        '''This method parses and returns the epoch date from the Two-Line Element (TLE). The epoch is a concept in astronomy
        which is a moment in time, that serves as reference point for some astronomical quantity. This method returns the epoch
        as a datetime object.

        :param tle: The Two-Line Element (TLE).
        :return: The epoch (Datetime Object).
        '''
        epoch = self.epoch(tle)
        year = self.epoch_year(tle, full_year=True)
        return datetime(year=year, month=1, day=1, tzinfo=tz.utc) + timedelta(days=epoch-1)

    def inclination(self, tle:str=None) -> float:
        '''This method parses and returns the orbital inclination of the satellite from the Two-Line Element (TLE). The orbital inclincation
        is the average angle between the equator and the orbit plane. The value provided is the TEME mean inclination. (NASA 1)

        Definition Citation:
        1. “Definition of Two-line Element Set Coordinate System.” SpaceFlight, National Aeronautics and Space Administration,
                23, Sept. 2011, https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html.

        :param tle: The Two-Line Element (TLE).
        :return: the TEME mean inclination.
        '''
        return self.individual_element(tle,2,8,16,func=float)

    def right_ascension(self, tle:str=None) -> float:
        '''This method parses and returns the right ascension of the satellites orbit from the Two-Line Element (TLE).
        The right ascension parameter from a TLE denotes the angle between vernal equinox and the point where
        the orbit crosses the equatorial plane in the Northern direction. The specific right ascenion parameter
        derived from the TLE is the TEME mean right ascension of the ascending node. (NASA 1)

        Definition Citation:
        1. “Definition of Two-line Element Set Coordinate System.” SpaceFlight, National Aeronautics and Space Administration,
                23, Sept. 2011, https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html.

        :param tle: The Two-Line Element (TLE).
        :return: the TEME mean right ascension of the ascending node.
        '''
        return self.individual_element(tle,2,17,25,func=float)

    def eccentricity(self, tle:str=None) -> float:
        '''This method parses and returns the orbital eccentricity from the Two-Line Element (TLE). The eccentricity of an
        astronomical object is a parameter that defines the shape of an orbit. The closer the eccentricity parameter
        is to 0, the more circular the orbit. The closer the eccentricity parameter is to 1 the more elliptical the orbit.
        Any eccentricity greater than a 1, the orbit is a parabolic escape orbit. The value supplied in the TLE is the
        average eccentricity. (NASA 1)

        Definition Citation:
        1. “Definition of Two-line Element Set Coordinate System.” SpaceFlight, National Aeronautics and Space Administration,
                23, Sept. 2011, https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html.

        :param tle: The Two-Line Element (TLE).
        :return: the average eccentricity parameter.
        '''
        return self.individual_element(tle,2,26,33,func=self.decimal_conversion)

    def argument_periapsis(self, tle:str=None) -> float:
        '''This method parses and returns the argument of periapsis of the satellites orbit from the Two-Line Element (TLE).
        The argument of periapsis is the angle between the ascending node and the orbit's point of closest approach to
        the earth, otherwise known as the orbit's "perigee". The term "perigee" is in the term used exlcusively for
        geocentric orbits, but is a specification on the more broad term "periapsis". The value provided in the TLE is
        the TEME mean argument of perigee.

        Definition Citation:
        1. “Definition of Two-line Element Set Coordinate System.” SpaceFlight, National Aeronautics and Space Administration,
                23, Sept. 2011, https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html.

        :param tle: The Two-Line Element (TLE).
        :return: the TEME Mean Argument of Perigee. (Degrees)
        '''
        return self.individual_element(tle,2,34,42,func=float)

    def mean_anomaly(self, tle:str=None) -> float:
        '''This method parses and returns the mean anomaly of the satellites orbit from the Two-Line Element (TLE).
        The mean anomaly parameter measures the angle from satellite's perigee, of the satellite location in the orbit
        referenced to a circular orbit with radius equal to the semi-major axis. (NASA 1) The mean anomaly can be thought of as
        the fraction of an elliptical orbit's period that has elapsed since the orbiting body passed perigee. (Wikipedia 2)

        Definition Citation:
        1. “Definition of Two-line Element Set Coordinate System.” SpaceFlight, National Aeronautics and Space Administration,
                23, Sept. 2011, https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html.

        2. “Mean Anomaly.” Wikipedia,
                17, Jan. 2019, https://en.wikipedia.org/wiki/Mean_anomaly.

        :param tle: The Two-Line Element (TLE).
        :return: the Mean Anomaly (Degrees)
        '''
        return self.individual_element(tle,2,43,51,func=float)

    def mean_motion(self, tle:str=None) -> float:
        '''This method parses and returns the mean motion of the satellites orbit from the Two-Line Element (TLE). The
        value returned from this method is the mean number of orbits per day the object completes. (NASA 1)

        Definition Citation:
        1. “Definition of Two-line Element Set Coordinate System.” SpaceFlight, National Aeronautics and Space Administration,
                23, Sept. 2011, https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html.

        :param tle: The Two-Line Element (TLE).
        :return: the Mean Motion (Average Number of Orbits/day).
        '''
        return self.individual_element(tle,2,52,63,func=float)

    def revolution(self, tle:str=None) -> float:
        '''This method parses and returns the satellites orbital revolution from the Two-Line Element (TLE). The orbit number
        at Epoch Time. This time is chosen very near the time of true ascending node passage as a matter of routine.
        (NASA 1)

        Definition Citation:
        1. “Definition of Two-line Element Set Coordinate System.” SpaceFlight, National Aeronautics and Space Administration,
                23, Sept. 2011, https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html.

        :param tle: The Two-Line Element (TLE).
        :return: the orbital Revolution (Number of Revolutions ).
        '''
        return self.individual_element(tle,2,63,68,func=float)

    def tle_to_dataframe(self, tle:str=None):
        '''This method take a Two-Line Element (TLE) and converts its elements into a Pandas DataFrame. This method is structured
        using slices of the TLE and then type conversions, as opposed to using the individual_element method intentionally.
        If we were to use the individual_element method we would iteratively call the parse_tle method which is ineffecient.
        So, for effeciency sake we will just call the parse_tle method once and then take a slice from it.

        :param tle: The Two-Line Element (TLE).
        :return: a Pandas DataFrame containing all of the elements within a TLE.
        '''
        title, line1, line2 =  self.parse_tle(tle=tle)
        sat_elements = {
            'title': title,
            'satellite_number': int(line1[2:7]),
            'classification': str(line1[7:8]),
            'international_designator_year': int(line1[9:11]),
            'international_designator_launch_number': int(line1[11:14]),
            'international_designator_piece_of_launch': str(line1[14:17]),
            'element_set_number': float(line1[64:68]),
            'inclination': float(line2[8:16]),
            'right_ascension': float(line2[17:25]),
            'eccentricity': self.decimal_conversion(line2[26:33]),
            'argument_periapsis': float(line2[34:42]),
            'mean_anomaly': float(line2[43:51]),
            'mean_motion': float(line2[52:63]),
            'epoch_date': self.epoch_date(tle=tle),
            'revolution': float(line2[63:68]),
            'bstar_drag_term': self.scientific_notation_conversion(line[53:61]),
            'second_time_derivative_of_mean_motion': self.scientific_notation_conversion(line1[44:52]),
            'ballistic_coeffecient': float(line1[33:43])
        }
        df = pd.DataFrame(sat_elements, index=[0])
        return df

    def satellite_orbital_elements(self, tle:str=None) -> tuple:
        '''This method parses and returns the Keplerian "Orbital" elements as individual components from the Two-Line Element (TLE).
        These elements are used by astronomers, scientists, and the US Military to understand the orbit of the satellite from the TLE.

        :param tle: The Two-Line Element (TLE).
        :return: The satellites keplerian elements. (i.e. a tuple containing the satellites Title, Inclination,
        Right Ascension, Eccentricty, Argument Perigee, Mean Anomaly and Motion, and Epoch Date)
        '''
        assert self.check_valid_tle(tle) is True, "Your TLE data failed the validity check. Confirm that the data is correct, and try again."

        title, line1, line2 =  self.parse_tle(tle)
        inclination = float(line2[8:16])
        right_ascension = float(line2[17:25])
        eccentricity = self.decimal_conversion(line2[26:33])
        argument_periapsis = float(line2[34:42])
        mean_anomaly = float(line2[43:51])
        mean_motion = float(line2[52:63])
        epoch_date = self.epoch_date(tle=tle)
        return title, inclination, right_ascension, eccentricity, argument_periapsis, mean_anomaly, mean_motion, epoch_date

    def satellite_identitfier_elements(self, tle:str=None) -> tuple:
        '''This method parses and returns the satellite's identifying elements as individual components from the Two-Line Element (TLE).
        These elements are used by astronomers, scientists, and the US Military to identify the satellite from the TLE.

        :param tle: The Two-Line Element (TLE).
        :return: The satellites identifying elements. (i.e. a tuple containing Satellite Number, Classification,
        International Designator Elements, and the Element Set Number)
        '''
        assert self.check_valid_tle(tle) is True, "Your TLE data failed the validity check. Confirm that the data is correct, and try again."

        title, line1, line2 =  self.parse_tle(tle=tle)
        satellite_number = int(line1[2:7])
        classification = str(line1[7:8])
        international_designator_year = int(line1[9:11])
        international_designator_launch_number = int(line1[11:14])
        international_designator_piece_of_launch = str(line1[14:17])
        element_set_number = float(line1[64:68])
        return satellite_number, classification, international_designator_year, international_designator_launch_number, international_designator_piece_of_launch, element_set_number
