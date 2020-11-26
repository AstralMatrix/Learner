"""TODO: INSERT DOCSTRING."""
import os.path
import json
from typing import List, Optional
from data_object import DataObject
from exception import error
from settings import Settings, SETTINGS_PATH


class FileReader:
    """TODO: INSERT DOCSTRING."""

    @staticmethod
    def read_files(file_paths: List[str]) -> Optional[List[DataObject]]:
        """Read the given files and loads in DataObjects from them.

        Currently supports the file formats '.json' and '.sfmt'

        Args:
            file_paths (List[str]): A list of all the files to be read.

        Returns:
            DataObject: All the elements that were loaded in from
                the files.
            None: If there was an error loading in any objects.
        """
        data: List[DataObject] = []
        for file_path in file_paths:
            file_path = os.path.join(Settings.directory_path, file_path)

            # Ensure the current file exists.
            if not os.path.exists(file_path):
                error(("unable to load file '{}', file could not be "
                       "found").format(file_path))
                return None

            if file_path.endswith('.json'):  # Json data file.
                if not FileReader.read_json(file_path, data):
                    return None
            elif file_path.endswith('.sfmt'):  # 'Simple Format' data file.
                if not FileReader.read_sfmt(file_path, data):
                    return None
            else:
                error(("the file '{}' is not a valid file format (.json or "
                       ".sfmt)").format(file_path))
                return None

        # Ensure that data was loaded in, and the files were not empty.
        if len(data) == 0:
            error("no elements were able to be found from any of the given "
                  "files")
            return None

        return data

    @staticmethod
    def read_json(file_path: str, data: List[DataObject]) -> bool:
        """Read in json files and adds the loaded DataObjects to `data`.

        Every json file should contain a 3D list of strings. The
        first dimention is the list containing all of the data
        for each DataObject. The second dimention is a representation
        of each DataObject. The third dimention is each 'segment' of
        the DataObject. Each segment contains strings representing
        the values for that segment.

        Args:
            file_path (str): The json file to be read.
            data (List[DataObject]): The list that the newly created
                data objects should be added to.

        Returns:
            bool: If all data was loaded properly (i.e. no errors).
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            # Read in the json from the file, if the json is valid.
            f_data: List[List[List[str]]]
            try:
                f_data = json.loads(f.read())
            except Exception as e:
                error("invalid json in file '{}' <{}>".format(file_path, e))
                return False

            # Ensure the data read from the file, and is a list as
            # expected.
            if f_data is None or not isinstance(f_data, list):
                error(("json in file '{}' does not contain a list as "
                       "expected").format(file_path))
                return False

            # Attempt to create a DataObject for each element in
            # the list read from the file.
            for elem in f_data:
                d_obj = DataObject.create_new(elem)
                # Ensure the DataObject was able to be successfully created.
                if d_obj is None:
                    error(("unable to create DataObject, invalid data from "
                           "file '{}': \"{}\"").format(file_path, elem))
                    return False
                data.append(d_obj)
        return True

    @staticmethod
    def read_sfmt(file_path: str, data: List[DataObject]) -> bool:
        """Read in sfmt files and adds the loaded DataObjects to `data`.

        sfmt stands for 'Simple Format' which is a file format designed
        to be simple and easy for the user to create.

        Each line in the file represents one DataObject. The lines
        use a '-' delimeter to seperate the segments for that
        DataObject, and each segment uses a '/' delimeter to seperate
        the segments into their respective values. This format does not
        use escape characters, meaning the '-' and '/' delimeters can
        not be used as part of regular text in the files, and should
        only be used to delimit their respective sections.

        An example line would be "this - is / a - test" which would
        turn into a DataObject with 3 segments consisting of
        [["this"], ["is", "a"], ["test"]].

        Args:
            file_path (str): The sfmt file to be read.
            data (List[DataObject]): The list that the newly created
                data objects should be added to.

        Returns:
            bool: If all data was loaded properly (i.e. no errors).
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                if line == "":
                    continue
                # Split the current line up into valid data for a DataObject
                line_data: List[List[str]] = \
                    [s.split("/") for s in line.split("-")]
                # Remove space formating from all strings.
                for segment in line_data:
                    for string in segment:
                        string = string.strip()

                d_obj = DataObject.create_new(line_data)
                # Ensure the DataObject was able to be successfully created.
                if d_obj is None:
                    error(("unable to create DataObject, invalid data from "
                           "file '{}': \"{}\"").format(file_path, line_data))
                    return False
                data.append(d_obj)
        return True

    @staticmethod
    def load_settings() -> None:
        """Read in the settings json file and sets the settings values.

        Returns:
            None
        """
        # Ensure the settings file exists.
        if not os.path.exists(SETTINGS_PATH):
            error(("unable to find settings file at '{}', please ensure it "
                   "exists. continuing to use default values"
                   ).format(SETTINGS_PATH))
            return

        with open(SETTINGS_PATH, 'r') as f:
            # Read in the json from the settings file, if the json is
            # valid. All data verification checks are done by Settings
            # when setting values, so none have to be done here.
            s_data: dict
            try:
                s_data = json.loads(f.read())
            except Exception as e:
                error(("invalid json in settings file '{}' <{}>. continuing "
                       "to use default values").format(SETTINGS_PATH, e))
                return
        # Load the settings from the new data. All data verification
        # checks are done by Settings when setting the new data.
        Settings.load_from(s_data)

    @staticmethod
    def save_settings() -> None:
        """Convert Settings to json string and save to the settings json file.

        Returns:
            None
        """
        # Ensure the settings file exists.
        if not os.path.exists(SETTINGS_PATH):
            error(("unable to find settings file at '{}', unable to save. "
                   "please ensure it exists").format(SETTINGS_PATH))
            return

        with open(SETTINGS_PATH, 'w') as f:
            f.write(Settings.as_json())
