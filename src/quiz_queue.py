from data_object import DataObject
from queue import Queue
from typing import List
from random import randint


class QuizQueue(object):

    def __init__(self, data: List[DataObject]):
        self.__data: List[DataObject] = data
        self.__queue: Queue = Queue()
        self.__last_item: DataObject = data[0]


    def __fill_queue(self):
        data_indicies: List[int] = [i for i in range(len(self.__data))]

        while len(data_indicies) != 0:
            curr_idx: int = randint(0, len(data_indicies) - 1)
            curr_item: DataObject = self.__data[data_indicies[curr_idx]]
            self.__queue.put(curr_item)
            del data_indicies[curr_idx]


    def recycle(self):
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
            idx += 1
        self.__queue = new_queue


    def next(self) -> DataObject:
        if self.__queue.empty():
            self.__fill_queue()

        ret_val: DataObject = self.__queue.get()
        self.__last_item = ret_val

        return ret_val