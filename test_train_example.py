import train_example
import unittest

class TestTrainExample(unittest.TestCase):

	def test_load(self):
		examples = train_example.load()

		print("X length: ", len(examples[0].x))
		print("Y length: ", len(examples[0].y))

		self.assertEqual(len(examples), 1)

if __name__ == '__main__':
    unittest.main()