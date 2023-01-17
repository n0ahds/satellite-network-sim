import unittest
from spaceman3D.Orbit import TLE, satellites

class setup_tests:

    def __init__(self):
        return

    def setup_wrong_tle_lengths(self) -> tuple:
        ''' We use this method to setup two test cases of Two-Line Elements (TLE) that have the incorrect number
        of lines. The method returns both of the different test cases. The first is the (long_tle) which has 4
        lines within the TLE, and the second is the (short_tle) which has 2 lines within the tle.

        :return: Two incorrect length Two-Line Elements (TLE)
        '''

        long_tle = """ISS (ZARYA)
                      1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
                      2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537
                      3 234 5678"""

        short_tle= """1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
                      2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537"""

        return long_tle, short_tle

    def setup_wrong_tle(self) -> tuple:
        ''' We use this method to setup three test cases of Two-Line Elements (TLE) that is the correct length
        of lines, but each have several incorrect features about them. The first  that we create has an incorrect checksum
        value at the end of line 1. The second has the wrong satellite number, and the third has an incorrect line
        number.

        :return: Three incorrect Two-Line Elements (TLE)
        '''

        wrong_chksum =  """ISS (ZARYA)
                           1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2928
                           2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537"""

        wrong_satnum = """ISS (ZARYA)
                          1 25543U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
                          2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537"""

        wrong_linenum = """ISS (ZARYA)
                           1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
                           9 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537"""

        return wrong_chksum, wrong_satnum, wrong_linenum

class TestSpaceman(unittest.TestCase):

################ TLE().parse_tle() #################
    #1
    def test_parse_tle_integer(self):
        '''This test is for the TLE().parse_tle() method and checks that the AssertionError is raised when
        an integer is passed in to the (tle) parameter of the method.'''
        integer = 1
        with self.assertRaises(AssertionError):
            TLE().parse_tle(tle=integer)
    #2
    def test_parse_tle_bool(self):
        '''This test is for the TLE().parse_tle() method and checks that the AssertionError is raised when
        an bool value is passed in to the (tle) parameter of the method.'''
        bool = True
        with self.assertRaises(AssertionError):
            TLE().parse_tle(tle=bool)
    #3
    def test_parse_tle_float(self):
        '''This test is for the TLE().parse_tle() method and checks that the AssertionError is raised when
        an float value is passed in to the (tle) parameter of the method.'''
        float = 1.0
        with self.assertRaises(AssertionError):
            TLE().parse_tle(tle=float)
    #4
    def test_parse_tle_short_length(self):
        '''This test is for the TLE().parse_tle() method and checks that the AssertionError is raised when
        a tle that has less than three lines is is passed in to the (tle) parameter of the method.'''
        long_tle, short_tle = setup_tests().setup_wrong_tle_lengths()
        with self.assertRaises(AssertionError):
            TLE().parse_tle(tle=short_tle)
    #5
    def test_parse_tle_long_length(self):
        '''This test is for the TLE().parse_tle() method and checks that the AssertionError is raised when
        a tle that has more than three lines is is passed in to the (tle) parameter of the method.'''
        long_tle, short_tle = setup_tests().setup_wrong_tle_lengths()
        with self.assertRaises(AssertionError):
            TLE().parse_tle(tle=long_tle)
    #6
    def test_parse_tle_return(self):
        '''This test is for the TLE().parse_tle() method and checks that the variables that the method returns
        are each the correct data type (String).'''
        title, line1, line2 = TLE().parse_tle(satellites.Dragon)
        self.assertIsInstance(title, str)
        self.assertIsInstance(line1, str)
        self.assertIsInstance(line2, str)


################ TLE().tle_checksum_algortithm() #################
    #7
    def test_checksum_algorithm_integer(self):
        '''This test is for the TLE().tle_checksum_algorithm() method and checks that the AssertionError is raised when
        an integer is passed in to the (line) parameter of the method.'''
        integer = 1
        with self.assertRaises(AssertionError):
            TLE().tle_checksum_algortithm(line=integer)
    #8
    def test_checksum_algorithm_bool(self):
        '''This test is for the TLE().tle_checksum_algorithm() method and checks that the AssertionError is raised when
        a bool value is passed in to the (line) parameter of the method.'''
        bool = True
        with self.assertRaises(AssertionError):
            TLE().tle_checksum_algortithm(line=bool)
    #9
    def test_checksum_algorithm_float(self):
        '''This test is for the TLE().tle_checksum_algorithm() method and checks that the AssertionError is raised when
        an float is passed in to the (line) parameter of the method.'''
        float = 1.0
        with self.assertRaises(AssertionError):
            TLE().tle_checksum_algortithm(line=float)
    #10
    def test_checksum_algorithm_return(self):
        '''This test is for the TLE().tle_checksum_algorithm() method and checks that the variables returned from the method
        are the expected data type (String)'''
        title, line1, line2 = TLE().parse_tle(satellites.Dragon)
        self.assertIsInstance(TLE().tle_checksum_algortithm(line1), str)
        self.assertIsInstance(TLE().tle_checksum_algortithm(line2), str)

    #11
    def test_checksum_algorithm_calc_check(self):
        '''This test is for the TLE().tle_checksum_algorithm() method and checks that calculation for the method is correct.'''
        title, line1, line2 = TLE().parse_tle(satellites.Dragon)
        self.assertEqual(TLE().tle_checksum_algortithm(line1), '8')
        self.assertEqual(TLE().tle_checksum_algortithm(line2), '6')

################ TLE().validation_framework() #################
    #12
    def test_validation_framework_integer_condtion1_single(self):
        '''This test is for the TLE().validation_framework() method and checks that the AssertionError is raised when
        an integer is passed in to the (condition1) parameter of the method.'''
        condition = 1
        expected = '1'
        with self.assertRaises(AssertionError):
            TLE().validation_framework(condition1=condition, expected1=expected, dual_condition=False)
    #13
    def test_validation_framework_integer_expected1_single(self):
        '''This test is for the TLE().validation_framework() method and checks that the AssertionError is raised when
        an integer is passed in to the (expected1) parameter of the method.'''
        condition = '1'
        expected = 1
        with self.assertRaises(AssertionError):
            TLE().validation_framework(condition1=condition, expected1=expected, dual_condition=False)
    #14
    def test_validation_framework_float_condtion1_single(self):
        '''This test is for the TLE().validation_framework() method and checks that the AssertionError is raised when
        a float is passed in to the (condition1) parameter of the method.'''
        condition = 1.0
        expected = '1'
        with self.assertRaises(AssertionError):
            TLE().validation_framework(condition1=condition, expected1=expected, dual_condition=False)
    #15
    def test_validation_framework_float_expected1_single(self):
        '''This test is for the TLE().validation_framework() method and checks that the AssertionError is raised when
        a float is passed in to the (expected1) parameter of the method.'''
        condition = '1'
        expected = 1.0
        with self.assertRaises(AssertionError):
            TLE().validation_framework(condition1=condition, expected1=expected, dual_condition=False)
    #16
    def test_validation_framework_bool_condtion1_single(self):
        '''This test is for the TLE().validation_framework() method and checks that the AssertionError is raised when
        a bool value is passed in to the (condition1) parameter of the method.'''
        condition = True
        expected = '1'
        with self.assertRaises(AssertionError):
            TLE().validation_framework(condition1=condition, expected1=expected, dual_condition=False)
    #17
    def test_validation_framework_bool_expected1_single(self):
        '''This test is for the TLE().validation_framework() method and checks that the AssertionError is raised when
        a bool value is passed in to the (expected1) parameter of the method.'''
        condition = '1'
        expected = False
        with self.assertRaises(AssertionError):
            TLE().validation_framework(condition1=condition, expected1=expected, dual_condition=False)
    #18
    def test_validation_framework_integer_condtion2_dual(self):
        '''This test is for the TLE().validation_framework() method and checks that the AssertionError is raised when
        an integer is passed in to the (condition2) parameter of the method.'''
        condition = 1
        expected = '1'
        with self.assertRaises(AssertionError):
            TLE().validation_framework(condition1='1', expected1='1', condition2=condition, expected2=expected)
    #19
    def test_validation_framework_integer_expected2_dual(self):
        '''This test is for the TLE().validation_framework() method and checks that the AssertionError is raised when
        an integer is passed in to the (expected2) parameter of the method.'''
        condition = '1'
        expected = 1
        with self.assertRaises(AssertionError):
            TLE().validation_framework(condition1='1', expected1='1', condition2=condition, expected2=expected)
    #20
    def test_validation_framework_float_condtion2_dual(self):
        '''This test is for the TLE().validation_framework() method and checks that the AssertionError is raised when
        a float is passed in to the (condition2) parameter of the method.'''
        condition = 1.0
        expected = '1'
        with self.assertRaises(AssertionError):
            TLE().validation_framework(condition1='1', expected1='1', condition2=condition, expected2=expected)
    #21
    def test_validation_framework_float_expected2_dual(self):
        '''This test is for the TLE().validation_framework() method and checks that the AssertionError is raised when
        a float is passed in to the (expected2) parameter of the method.'''
        condition = '1'
        expected = 1.0
        with self.assertRaises(AssertionError):
            TLE().validation_framework(condition1='1', expected1='1', condition2=condition, expected2=expected)
    #22
    def test_validation_framework_bool_condtion2_dual(self):
        '''This test is for the TLE().validation_framework() method and checks that the AssertionError is raised when
        a bool value is passed in to the (condition2) parameter of the method.'''
        condition = True
        expected = '1'
        with self.assertRaises(AssertionError):
            TLE().validation_framework(condition1='1', expected1='1', condition2=condition, expected2=expected)
    #23
    def test_validation_framework_bool_expected2_dual(self):
        '''This test is for the TLE().validation_framework() method and checks that the AssertionError is raised when
        a bool value is passed in to the (expected2) parameter of the method.'''
        condition = '1'
        expected = False
        with self.assertRaises(AssertionError):
            TLE().validation_framework(condition1='1', expected1='1', condition2=condition, expected2=expected)
    #24
    def test_validation_framework_str_dual(self):
        '''This test is for the TLE().validation_framework() method and checks that the AssertionError is raised when
        a string is passed in to the (dual_condition) parameter of the method.'''
        dual_condition = '1'
        with self.assertRaises(AssertionError):
            TLE().validation_framework(condition1='1', expected1='1', condition2="1", expected2="1", dual_condition=dual_condition)
    #25
    def test_validation_framework_int_dual(self):
        '''This test is for the TLE().validation_framework() method and checks that the AssertionError is raised when
        a integer is passed in to the (dual_condition) parameter of the method.'''
        dual_condition = 1
        with self.assertRaises(AssertionError):
            TLE().validation_framework(condition1='1', expected1='1', condition2="1", expected2="1", dual_condition=dual_condition)
    #26
    def test_validation_framework_float_dual(self):
        '''This test is for the TLE().validation_framework() method and checks that the AssertionError is raised when
        a float is passed in to the (dual_condition) parameter of the method.'''
        dual_condition = 1.0
        with self.assertRaises(AssertionError):
            TLE().validation_framework(condition1='1', expected1='1', condition2="1", expected2="1", dual_condition=dual_condition)
    #28
    def test_validation_framework_return_dual(self):
        '''This test is for the TLE().validation_framework() method and checks that the variables returned from the method
        in a single condition test are the expected data type (Bool)'''
        self.assertIsInstance(TLE().validation_framework(condition1='1', expected1='1', condition2="1", expected2="1"), bool)
    #29
    def test_validation_framework_return_single(self):
        '''This test is for the TLE().validation_framework() method and checks that the variables returned from the method
        in a dual condition test are the expected data type (Bool)'''
        self.assertIsInstance(TLE().validation_framework(condition1='1', expected1='1', dual_condition=False), bool)
    #30
    def test_validation_framework_calc_check_dual(self):
        '''This test is for the TLE().validation_framework() method and and checks that calculation for the method is correct.'''
        self.assertEqual(TLE().validation_framework(condition1='1', expected1='1', condition2="1", expected2="1"), True)
        self.assertEqual(TLE().validation_framework(condition1='1', expected1='2', condition2="1", expected2="1"), False)
        self.assertEqual(TLE().validation_framework(condition1='1', expected1='1', condition2="1", expected2="2"), False)
        self.assertEqual(TLE().validation_framework(condition1='1', expected1='2', condition2="1", expected2="2"), False)
    #31
    def test_validation_framework_calc_check_single(self):
        '''This test is for the TLE().validation_framework() method and and checks that calculation for the method is correct. '''
        self.assertEqual(TLE().validation_framework(condition1='1', expected1='1', dual_condition=False), True)
        self.assertEqual(TLE().validation_framework(condition1='1', expected1='2', dual_condition=False), False)

################ TLE().check_valid_tle() #################
    #32
    def test_check_valid_tle_return(self):
        '''This test is for the TLE().check_valid_tle() method and checks that the variable returned from the method
        are the expected data type (Bool)'''
        wrong_chksum, wrong_satnum, wrong_linenum = setup_tests().setup_wrong_tle()
        self.assertIsInstance(TLE().check_valid_tle(satellites.Dragon), bool)
        self.assertIsInstance(TLE().check_valid_tle(wrong_chksum), bool)
        self.assertIsInstance(TLE().check_valid_tle(wrong_satnum), bool)
        self.assertIsInstance(TLE().check_valid_tle(wrong_linenum), bool)
    #33
    def test_check_valid_tle_calc_check(self):
        '''This test is for the TLE().check_valid_tle() method and and checks that calculation for the method is correct. '''
        wrong_chksum, wrong_satnum, wrong_linenum = setup_tests().setup_wrong_tle()
        self.assertEqual(TLE().check_valid_tle(satellites.Dragon), True)
        self.assertEqual(TLE().check_valid_tle(wrong_chksum), False)
        self.assertEqual(TLE().check_valid_tle(wrong_satnum), False)
        self.assertEqual(TLE().check_valid_tle(wrong_linenum), False)

################ TLE().scientific_notation_conversion() #################
    #34
    def test_scientific_notation_conversion_calc_check(self):
        '''This test is for the TLE().scientific_notation_conversion() method and and checks that calculation for the method is correct. '''
        self.assertEqual(TLE().scientific_notation_conversion('-01234-5'), -1.2340000000000004e-06)
        self.assertEqual(TLE().scientific_notation_conversion(' 01234-5'), 1.2340000000000004e-06)
        self.assertEqual(TLE().scientific_notation_conversion(' 01234+5'), 12340.000000000002)
        self.assertEqual(TLE().scientific_notation_conversion('-01234+5'), -12340.000000000002)
        self.assertEqual(TLE().scientific_notation_conversion(' 00000+0'), 0.0)
        self.assertEqual(TLE().scientific_notation_conversion(' 00000-0'), 0.0)

    #35
    def test_scientific_notation_conversion_integer(self):
        '''This test is for the TLE().scientific_notation_conversion() method and checks that the AssertionError is raised when
        an integer is passed in to the (element) parameter of the method.'''
        integer = 1
        with self.assertRaises(AssertionError):
            TLE().scientific_notation_conversion(element=integer)
    #36
    def test_scientific_notation_conversion_float(self):
        '''This test is for the TLE().scientific_notation_conversion() method and checks that the AssertionError is raised when
        an float is passed in to the (element) parameter of the method.'''
        float = 1.0
        with self.assertRaises(AssertionError):
            TLE().scientific_notation_conversion(element=float)
    #37
    def test_scientific_notation_conversion_bool(self):
        '''This test is for the TLE().scientific_notation_conversion() method and checks that the AssertionError is raised when
        an bool is passed in to the (element) parameter of the method.'''
        bool = True
        with self.assertRaises(AssertionError):
            TLE().scientific_notation_conversion(element=True)
    #38
    def test_scientific_notation_conversion_short_length(self):
        '''This test is for the TLE().scientific_notation_conversion() method and checks that the AssertionError is raised when
        a short value is passed in to the (element) parameter of the method.'''
        with self.assertRaises(AssertionError):
            TLE().scientific_notation_conversion(element='0001-1')
    #39
    def test_scientific_notation_conversion_long_length(self):
        '''This test is for the TLE().scientific_notation_conversion() method and checks that the AssertionError is raised when
        a long value is passed in to the (element) parameter of the method.'''
        with self.assertRaises(AssertionError):
            TLE().scientific_notation_conversion(element='00000001-1')

if __name__ == "__main__":
    unittest.main()
