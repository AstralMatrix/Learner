"""TODO: INSERT DOCSTRING."""
from typing import List, Optional

from package.src.file_reader import FileReader
from package.src.data_object import DataObject
from package.src.quiz_queue import QuizQueue


# Data object displaying that an error occured.
ERROR_D_OBJ: DataObject = DataObject([["No objects were able to be loaded"]])


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
        self.__curr_element: DataObject = None

        # Track the satistics of the total number of quiz elements, and the
        # number the user got correct.
        self.__total_items: int = 0
        if self.__raw_data is not None:
            self.__total_items = len(self.__raw_data)
        self.__number_correct: int = 0

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
        else:
            self.__number_correct += 1
        return is_correct

    @property
    def total_number_of_items(self) -> int:
        """Get the total number of elements loaded."""
        return self.__total_items

    @property
    def number_of_correct_items(self) -> int:
        """Get the number of elements the user got correct."""
        return self.__number_correct

    @property
    def percent_correct(self) -> int:
        """Get the percent of total elements the user got correct."""
        if self.__total_items == 0:
            return 0
        return int((self.__number_correct / self.__total_items) * 100)
