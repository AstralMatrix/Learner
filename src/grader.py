"""TODO: INSERT DOCSTRING."""
from file_reader import FileReader
from data_object import DataObject
from quiz_queue import QuizQueue
from typing import List, Optional


# Data object displaying that an error occured.
ERROR_D_OBJ: DataObject = DataObject([["ERROR"]])


class Grader:
    """Simple grading object to control question grading.

    Used by the main form to grade and display questions (data objects) to
    help remove the QuizQueue overhead. Utilizes the QuizQueue for storing
    and getting data objects.
    """

    def __init__(self, file_paths: List[str]):
        """TODO: INSERT DOCSTRING."""
        # Load in all data objects from the given files.
        self.__raw_data: Optional[List[DataObject]] = \
            FileReader.read_files(file_paths)

        # Display error data object if loading failed.
        if self.__raw_data is None:
            self.__raw_data = [ERROR_D_OBJ]

        # Create a quiz queue to randomize the elements.
        self.__elements: QuizQueue = QuizQueue(self.__raw_data)
        self.__curr_element: DataObject = self.__elements.dequeue()

    def get_display_question(self, segment_idx: int) -> str:
        """Get the segment of a data object.

        The given segment represents the question to be displayed.

        Args:
            segment_idx (int): The index of the desired segment.

        Returns:
            str: The string representation of the given segment.
        """
        return self.__curr_element.segment_str(segment_idx)

    def get_display_answer(self) -> str:
        """Display the entire data object.

        This represents the answer to the question to be displayed.

        Returns:
            str: The string representation of the given data object.
        """
        return str(self.__curr_element)

    def next(self) -> None:
        """Move on to the next data object from the quiz queue."""
        self.__curr_element = self.__elements.dequeue()

    def check(self, input_str: str) -> bool:
        """Check if the input string is correct for the current data object.

        Recycle the data object back into the quiz queue if it is not.

        Args:
            input_str (str): The string to be checked.

        Returns:
            bool: If the input string was correct or not.
        """
        is_correct: bool = self.__curr_element.check(input_str)
        # If the answer is wrong add it back in near the front of the
        # queue, so it can be given again.
        if not is_correct:
            self.__elements.recycle()
        return is_correct
