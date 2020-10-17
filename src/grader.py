from file_reader import FileReader
from data_object import DataObject
from quiz_queue import QuizQueue
from typing import List


ERROR_D_OBJ: DataObject = DataObject([["ERROR"]])


class Grader(object):

    def __init__(self, file_paths: List[str]):
        self.__raw_data: List[DataObject] = FileReader.read_files(file_paths)

        if self.__raw_data is None:
            self.__raw_data = [ERROR_D_OBJ]

        self.__elements: QuizQueue = QuizQueue(self.__raw_data)
        self.__curr_element: DataObject = self.__elements.next()


    def get_display_question(self, segment_idx: int) -> str:
        return self.__curr_element.segment_str(segment_idx)


    def get_display_answer(self) -> str:
        return str(self.__curr_element)


    def next(self) -> None:
        self.__curr_element = self.__elements.next()

    
    def check(self, input_str: str) -> bool:
        is_correct: bool = self.__curr_element.check(input_str)
        # If the answer is wrong add it back in near the front of the
        # queue, so it can be given again.
        if not is_correct:
            self.__elements.recycle()
        return is_correct
