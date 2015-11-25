import train
import unittest

class TestTrain(unittest.TestCase):

	def test_train(self):
		w = train.train()
		print("w:", w)

		self.assertEqual(len(w), 1)

if __name__ == '__main__':
    unittest.main()