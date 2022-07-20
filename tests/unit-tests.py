import sys
sys.path.insert(0, '../src')
import vader
import unittest

class TestVader(unittest.TestCase):


	def setUp(self):
		self.testDbData = [(241676000, 'UnderWayUsingEngine', 11.8, 237.0, 48.646162, -68.70876, 237), (241676000, 'UnderWayUsingEngine', 11.8, 236.4, 48.644912, -68.711683, 236), (241676000, 'UnderWayUsingEngine', 11.8, 236.2, 48.644365, -68.71293, 236), (241676000, 'UnderWayUsingEngine', 11.8, 236.6, 48.642537, -68.717067, 237), (246716000, 'UnderWayUsingEngine', 13.1, 56.0, 48.477167, -68.913667, 55)]

	def test_build_training_data(self):
		
		dataStruct = vader.build_training_data(self.testDbData)
		assert(len(dataStruct[0]) == 6)
	
	def test_get_points(self):
		points = vader.get_points(self.testDbData)
		self.assertEqual(points[0][0], 48.646162)
		self.assertEqual(points[0][1], -68.70876)

if __name__ == '__main__':
    unittest.main()
