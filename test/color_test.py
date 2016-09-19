import unittest


class ColorTest(unittest.TestCase):
    def test_opposite(self):
        from lib.color_compliment import getOppositeColor

        R, G, B = getOppositeColor(0, 96, 22)

        assert 0 <= R and R <= 255
        assert 0 <= G and G <= 255
        assert 0 <= B and B <= 255


if __name__ == '__main__':
    import sys
    sys.path.insert(0, '.')
    unittest.main()
