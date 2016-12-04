import unittest

class SanityTest(unittest.TestCase):

    def test_sanity(self):
        """
        Tests the sanity of the unit testing framework and if we can import all
        we need to work
        """
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
