from DataTransformation.transformation import *
import unittest

class TestTransformationMethods(unittest.TestCase):

    def test_TotalVisitorAmountTransformation(self):
        self.assertEqual(transformTotalVisitorsToInt("30M"), 30000000)
        self.assertEqual(transformTotalVisitorsToInt("25.47K"), 25470)
        with self.assertRaises(ValueError):
            transformTotalVisitorsToInt("30X")

    def test_TransformAvgVisitDurationTransformation(self):
        self.assertEqual(transformAvgVisitDurationToSeconds("00:04:18"),258)
        self.assertEqual(transformAvgVisitDurationToSeconds("02:04:18"),7458)
        with self.assertRaises(ValueError):
            transformAvgVisitDurationToSeconds("00:70:70")
        with self.assertRaises(ValueError):
            transformAvgVisitDurationToSeconds("04:18")
        with self.assertRaises(ValueError):
            transformAvgVisitDurationToSeconds("03.2")

    def test_JumpOffRateTransformation(self):
        self.assertEqual(transformJumpOffRateToFloat("45.32%"), 45.32)
        with self.assertRaises(ValueError):
            transformJumpOffRateToFloat("XXX")

    def test_PriceTransformation(self):
        self.assertEqual(transformPriceToFloat("30,2"), 30.2)
        self.assertEqual(transformPriceToFloat("30,2€"), 30.2)
        self.assertEqual(transformPriceToFloat("30.2€"), 30.2)
        with self.assertRaises(ValueError):
            transformPriceToFloat("XXX")

    def test_PriceTransformationEuronics(self):
        self.assertEqual(transformPriceToFloatEuronics("30,2"), 30.2)
        self.assertEqual(transformPriceToFloatEuronics("30,2€"), 30.2)
        self.assertEqual(transformPriceToFloatEuronics("30.2€"), 30.2)
        with self.assertRaises(ValueError):
            transformPriceToFloatEuronics("XXX")

    def test_transformMonthYearToTimestamp(self):
        self.assertEqual(transformMonthYearToTimestamp("Februar 2022"), datetime.datetime.strptime("02/2022", "%m/%Y"))
        self.assertEqual(transformMonthYearToTimestamp("March 2022"), datetime.datetime.strptime("03/2022", "%m/%Y"))
        with self.assertRaises(ValueError):
            transformMonthYearToTimestamp("XXX")

    def test_transformShareToFloat(self):
        self.assertEqual(transformShareToFloat("62.92%"), 62.92)

if __name__ == '__main__':
    unittest.main()