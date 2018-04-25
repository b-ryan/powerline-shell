import unittest
from parameterized import parameterized

from powerline_shell.color_compliment import getOppositeColor


def build_inputs():
    
    # Build 768 hex/rgb values to test against getOppositeColor
    input_bytes = map(hex, xrange(pow(2,8)))

    input_list = []
    for x in input_bytes:

        #Building hex range of [00-ff]:00:00
        combined1 = hex((int(x,16)<<16)| ((int(input_bytes[0],16)<<8)|int(input_bytes[0],16))) 
        test_input1 = tuple((int(x,16), int(input_bytes[0],16), int(input_bytes[0],16)))

        #Building hex range of 00:[00-ff]:00
        combined2 = hex((int(input_bytes[0],16)<<16)| ((int(x,16)<<8)|int(input_bytes[0],16)))
        test_input2 = tuple((int(input_bytes[0],16), int(x,16), int(input_bytes[0],16))) 

        #Building hex range of 00:00:[00-ff]
        combined3 = hex((int(input_bytes[0],16)<<16)| ((int(input_bytes[0],16)<<8)|int(x,16)))
        test_input3 = tuple((int(input_bytes[0],16), int(input_bytes[0],16), int(x,16))) 

        input_list.append(tuple((combined1, test_input1)))
        input_list.append(tuple((combined2, test_input2)))
        input_list.append(tuple((combined3, test_input3)))

    return input_list

class getOppositeColorTestCase(unittest.TestCase):

    '''
    Test only runs against 768 combinations of rgb values. 
    Trying to run parameterized unittest against 16.77M rgb values
    was near impossible (need lots of memory and time).  Of the 768 
    values tested, the test has proven to catch 192 exceptions (and 3
    ZeroDivisionError exceptions from rgb_to_hls).  This can be tested
    by commenting out the first line of getOppositeColor, which 
    converts the rgb values to float.
    '''

    @parameterized.expand(build_inputs)
 
    def test_rgb_input_get_opposite_not_negative(self, name, test_input):
        negative = -1
        self.assertNotIn(negative, getOppositeColor(*test_input), u'{0:#08x} returns negative number in rgb tuple'.format(int(name,16)))
