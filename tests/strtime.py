import unittest

from wicamp.strtime import to_minutes, strtime_diff


class TestSum(unittest.TestCase):
    def test_to_mintues(self):
        self.assertEqual(to_minutes("0min"), 0)
        self.assertEqual(to_minutes("27min"), 27)
        self.assertEqual(to_minutes("54min"), 54)
        self.assertEqual(to_minutes("1h 0min"), 60)
        self.assertEqual(to_minutes("3h 22min"), 202)
        self.assertEqual(to_minutes("6h 35min"), 395)

    def test_strtime_diff(self):
        self.assertEqual(strtime_diff("6h 0min", "1h 0min"), 300)
        self.assertEqual(strtime_diff("3h 22min", "15min"), 187)
        self.assertEqual(strtime_diff("3h 22min", "3h 22min"), 0)
        self.assertEqual(strtime_diff("2h 39min", "4h 53min"), 134)


if __name__ == '__main__':
    unittest.main()
