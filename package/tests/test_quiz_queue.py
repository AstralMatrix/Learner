"""TODO: INSERT DOCSTRING."""
import unittest
from typing import List

from package.src.quiz_queue import QuizQueue
from package.src.data_object import DataObject


class TestQuizQueue(unittest.TestCase):
    """Tests for verifying the QuizQueue."""

    def test_create(self):
        """Ensure the queue is created with the proper number of elements."""
        # Test multiple different insertion lengths.
        for i in range(1, 200):
            # Create and populate test list to be inserted.
            queue_insert_list: List[DataObject] = list()
            for j in range(i):
                new_d_obj = DataObject.create_new([[str(j)]])
                self.assertNotEqual(new_d_obj, None)
                queue_insert_list.append(new_d_obj)

            # Create the queue and ensure it has the correct legnths.
            test_queue: QuizQueue = QuizQueue(queue_insert_list)
            self.assertEqual(test_queue.total_length, i)
            self.assertEqual(test_queue.length, 0)
            test_queue.dequeue()
            self.assertEqual(test_queue.length, i-1)
            self.assertEqual(test_queue.total_length, i)

    def test_remove(self):
        """Ensure the queue removes each element exactly once per refill."""
        # Test multiple different removal lengths.
        for i in range(1, 200):
            # Create and populate test list to be inserted.
            queue_insert_list: List[DataObject] = list()
            for j in range(i):
                new_d_obj = DataObject.create_new([[str(j)]])
                self.assertNotEqual(new_d_obj, None)
                queue_insert_list.append(new_d_obj)

            test_queue: QuizQueue = QuizQueue(queue_insert_list)
            out_list: List[DataObject] = list()

            # For i inserts do i removes, and ensure that every element has
            # been dequeued exactly once.
            for _ in range(i):
                out_list.append(test_queue.dequeue())

            for item in out_list:
                self.assertEqual(queue_insert_list.count(item), 1)

            for item in queue_insert_list:
                self.assertEqual(out_list.count(item), 1)

    def test_remove_with_recycle(self):
        """Ensure the queue recycles items properly exactly once."""
        # Test multiple different removal lengths.
        for i in range(1, 50):
            # Create and populate test list to be inserted.
            queue_insert_list: List[DataObject] = list()
            for j in range(i):
                new_d_obj = DataObject.create_new([[str(j)]])
                self.assertNotEqual(new_d_obj, None)
                queue_insert_list.append(new_d_obj)

            test_queue: QuizQueue = QuizQueue(queue_insert_list)
            out_list: List[DataObject] = list()

            # For i inserts do i * 2 removes and recycles, and ensure that
            # every element has been dequeued exactly twice. i * 2 elements
            # are removed to test that items are not recycled more than once.
            for _ in range(i * 2):
                out_list.append(test_queue.dequeue())
                test_queue.dequeue()
                test_queue.recycle()

            for item in out_list:
                self.assertEqual(queue_insert_list.count(item), 1)

            for item in queue_insert_list:
                self.assertEqual(out_list.count(item), 2)


if __name__ == '__main__':
    unittest.main()
