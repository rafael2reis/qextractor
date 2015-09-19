import unittest
from wis import Task
import wis

class TestWis(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sortTasksByEnd(self):
        print "test_sortTasksByEnd"

        tasks = [Task(0,2,1), Task(1,4,1), Task(0,1,1)]
        tasksSorted = [Task(0,1,1), Task(0,2,1), Task(1,4,1)]

        tasks = wis.sortTasksByEnd(tasks)

        ends = [t.end for t in tasks]
        endsSorted = [t.end for t in tasksSorted]

        print ends
        print endsSorted

        self.assertEqual(ends, endsSorted)

    def test_createPreviousArray(self):
        print "test_createPreviousArray"

        tasks = [Task(0,0,0), Task(0,1,1), Task(0,2,1), 
                        Task(1,4,1), Task(4,5,1), Task(2,6,1), Task(5,7,1)]

        p = wis.createPreviousArray(tasks)
        pCorrect = [0, 0, 0, 1, 3, 2, 4]

        print p
        print pCorrect

        self.assertEqual(p, pCorrect)

    def test_schedule(self):
        print "test_schedule"

        tasks = [Task(0,1,1), Task(0,2,1), 
                        Task(1,4,1), Task(4,5,1), Task(2,6,1), Task(5,7,1)]

        set_correct = [Task(0,1,1), Task(1,4,1), Task(4,5,1), Task(5,7,1)]
        max_w, set_tasks = wis.schedule(tasks)

        print set_correct
        print set_tasks

        self.assertEqual(set_correct, set_tasks)


if __name__ == '__main__':
    unittest.main()