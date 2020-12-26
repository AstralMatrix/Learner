"""TODO: INSERT DOCSTRING."""
from typing import List
from random import randint
from typing import Optional


class DataObject:
    """Stores the data for an element to be displayed and checked.

    The data is a 2D array of strings. The first dimension is the
    segment. The second dimension is the all of the possible string
    values for that segment.

    The segments are broken up for display puropses, so the object
    can be represented by just a single segment instead of all of
    the data.

    Attributes:
        data (List[List[str]]): The data this object contains.

    Properties:
        segments (int): The number of segements the data contains.
    """

    def __init__(self, data: List[List[str]]) -> None:
        """TODO: INSERT DOCSTRING."""
        self.__data: List[List[str]] = data

    @property
    def segments(self) -> int:
        """Return the number of segments this object has."""
        return len(self.__data)

    def check(self, comare_str: str) -> bool:
        """Return if the comparison string is contained in this object's data.

        Args:
            compare_str (str): The string to be compared.

        Return:
            bool: If the object contained the input string.
        """
        comare_str = self._clean_string(comare_str)
        for segment in self.__data:
            for string in segment:
                if self._clean_string(string) == comare_str:
                    return True
        return False

    def segment_str(self, idx: int) -> str:
        """Return the string of the segment of data at the given index.

        Return a random segment if the index is negative, or index 0
        if the index is out of bounds.

        Args:
            idx (int): The index of the desired segment.

        Return:
            str: A string of the segment data.
        """
        # Randomize the index if it is negative, or set it to 0 if it
        # is out of bounds in the positive direction.
        if idx < 0:
            idx = randint(0, self.segments - 1)
        elif idx >= self.segments:
            idx = 0

        ret_val = ""
        for string in self.__data[idx]:  # Concat every part of the segment.
            ret_val += string + " | "
        # Return the new string except for the trailing " | ".
        return ret_val[:-3].strip()

    def __str__(self) -> str:
        """TODO: INSERT DOCSTRING."""
        ret_val: str = ""
        for i in range(self.segments):  # Concat every segment onto a new line.
            ret_val += self.segment_str(i) + "\n"
        if ret_val.strip() == "":  # Object has no data.
            return "[EMPTY_DATAOBJECT]"
        return ret_val.strip()

    @staticmethod
    def _clean_string(line: str) -> str:
        """Remove all formatting from the given string.

        This includes all ASCII symbols and spaces.

        Args:
            line (str): The string to be cleaned.

        Return:
            str: The cleaned string.
        """
        symbols: List[str] = [
            '~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-',
            '_', '=', '+', '[', ']', '{', '}', '|', '\\', ':', ';', '\'', '"',
            ',', '<', '.', '>', '/', '?']
        for s in symbols:
            line = line.replace(s, "")
        line = line.replace(" ", "")
        return line.lower().strip()

    @staticmethod
    def check_all(d_objs: List['DataObject'], compare_str: str) -> bool:
        """Return if any of the DataObjects contain the given string.

        Args:
            d_objs (List[DataObject]): The objects to be checked for
                the input string.
            compare_str (str): The string to be compared.

        Return:
            bool: If the input string was found in any of the DataObjects.
        """
        for d_obj in d_objs:
            if d_obj.check(compare_str):
                return True
        return False

    @staticmethod
    def verify(data: List[List[str]]) -> bool:
        """Return if the data given is well formated.

        Args:
            data (List[List[str]]): The data to be checked.

        Return:
            bool: If the input data is well formed.
        """
        # Ensure the data is a list.
        if not isinstance(data, list):
            return False

        # Ensure the data list only contains lists.
        for lst in data:
            if not isinstance(lst, list):
                return False

            # Ensure each inner list only contains strings.
            for string in lst:
                if not isinstance(string, str):
                    return False

        return True

    @staticmethod
    def create_new(data: List[List[str]]) -> Optional['DataObject']:
        """Return a new DataObject if the data provided is well formatted.

        Return None otherwise.

        Args:
            data (List[List[str]]): The data for the DataObject will
                store.

        Return:
            DataObject: The new object if the data is well formed.
            None: If the data is not well formed.
        """
        if DataObject.verify(data):
            return DataObject(data)
        return None
