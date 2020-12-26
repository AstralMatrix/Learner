"""TODO: INSERT DOCSTRING."""
from queue import Queue
from typing import List
from random import randint

from package.src.data_object import DataObject


class QuizQueue:
    """Queue to store DataObjects used to quiz the user.

    The queue automatically randomizes and refills itself every time it is
    empty. This means that 'next()' can be called indefinitly. This allows for
    the user to be quized on items randomly.
    """

    def __init__(self, data: List[DataObject]):
        """TODO: INSERT DOCSTRING."""
        # A list of all the DataObjects. This is used to refill the queue.
        self.__data: List[DataObject] = data
        self.__queue: Queue = Queue()
        # The most recent item to be dequeued.
        self.__last_item: DataObject = data[0]

    def __fill_queue(self) -> None:
        """Refill the queue in a random order."""
        # A list of the indicies of all the elements to be inserted.
        data_indicies: List[int] = list(range(len(self.__data)))

        while len(data_indicies) != 0:
            # Generate a random index from data_indicies to insert.
            curr_idx: int = randint(0, len(data_indicies) - 1)
            # Insert the DataObject from the given index, chosen by the random
            # index.
            curr_item: DataObject = self.__data[data_indicies[curr_idx]]
            self.__queue.put(curr_item)
            # Remove the index of object that was just inserted from the
            # so it isn't added more than once.
            del data_indicies[curr_idx]

    def recycle(self) -> None:
        """Re-insert the last dequeued item back toward the front of the queue.

        This is used in the case the user got a question wrong, so the same
        question will reappear shortly after.
        """
        new_queue: Queue = Queue()
        idx: int = 0
        # Add first 3 old items to the new queue.
        while not self.__queue.empty() and idx < 3:
            new_queue.put(self.__queue.get())
            idx += 1
        # Add the recycled element back into the new queue.
        new_queue.put(self.__last_item)
        # Finish copying the old queue items into the new queue.
        while not self.__queue.empty():
            new_queue.put(self.__queue.get())
        self.__queue = new_queue

    def dequeue(self) -> DataObject:
        """Dequeue and return the next element in the queue.

        Refill the queue if necessary.

        Returns:
            DataObject: The object the user should be quized on.
        """
        if self.__queue.empty():
            self.__fill_queue()

        ret_val: DataObject = self.__queue.get()
        self.__last_item = ret_val

        return ret_val

    @property
    def length(self) -> int:
        """Get the current length of the queue."""
        return self.__queue.qsize()

    @property
    def total_length(self) -> int:
        """Get the total length of the queue."""
        return len(self.__data)
