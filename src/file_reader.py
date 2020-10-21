import json
from typing import List
import os.path
from data_object import DataObject
from exception import error
from settings import Settings, SETTINGS_PATH


class FileReader:

    
    @staticmethod
    def read_files(file_paths: List[str]) -> List[DataObject]:
        '''Reads in json files and loads in DataObjects from them.

            Every json file should contain a 3D list of strings. The
            first dimention is the list containing all of the data
            for each DataObject. The second dimention is a representation
            of each DataObject. The third dimention is each 'segment' of
            the DataObject. Each segment contains strings representing
            the values for that segment.

            Args:
                file_paths (List[str]): A list of all the json file to
                    be read.

            Returns:
                DataObject: All the elements that were loaded in from
                    the files.
                None: If there was an error loading in any objects.
        '''
        data: List[DataObject] = []
        for file_path in file_paths:
            file_path = file_path.strip()

            # Ensure the current file exists.
            if not os.path.exists(file_path):
                error("unable to load file '{}', file could not be found". format(file_path))
                return None

            # Ensure the current file is a .json file.
            if file_path[-5:] != ".json":
                error("the file '{}' is not a .json file". format(file_path))
                return None

            with open(file_path, 'r') as f:
                # Read in the json from the file, if the json is valid.
                f_data: List[List[str]]
                try:
                    f_data = json.loads(f.read())
                except Exception as e:
                    error("invalid json in file '{}' <{}>".format(file_path, e))
                    return None

                # Ensure the data read from the file, and is a list as
                # expected.
                if f_data is None or type(f_data) != list:
                    error("json in file '{}' does not contain a list as expected".format(file_path))
                    return None

                # Attempt to create a DataObject for each element in
                # the list read from the file.
                for elem in f_data:
                    d_obj = DataObject.create_new(elem)
                    # Ensure the DataObject was able to be successfully
                    # created.
                    if d_obj is None:
                        error("unable to create DataObject, invalid data from file '{}': \"{}\"".format(file_path, elem))
                        return None
                    data.append(d_obj)

        # Ensure that data was loaded in, and the files were not empty.
        if len(data) == 0:
            error("no elements were able to be found from any of the given files")
            return None

        return data


    @staticmethod
    def load_settings() -> None:
        '''Reads in the settings json file and sets the settings values.

            Returns:
                None
        '''
        # Ensure the settings file exists.
        if not os.path.exists(SETTINGS_PATH):
            error("unable to find settings file at '{}', please ensure it exists. continuing to use default values". format(SETTINGS_PATH))
            return

        with open(SETTINGS_PATH, 'r') as f:
            # Read in the json from the settings file, if the json is
            # valid. All data verification checks are done by Settings
            # when setting values, so none have to be done here.
            s_data: dict
            try:
                s_data = json.loads(f.read())
            except Exception as e:
                error("invalid json in settings file '{}' <{}>. continuing to use default values".format(SETTINGS_PATH, e))
                return
        # Load the settings from the new data. All data verification
        # checks are done by Settings when setting the new data.
        Settings.load_from(s_data)

    
    @staticmethod
    def save_settings() -> None:
        '''Converts Settings to a json string and saves it to the settings json file.

            Returns:
                None
        '''
        # Ensure the settings file exists.
        if not os.path.exists(SETTINGS_PATH):
            error("unable to find settings file at '{}', unable to save. please ensure it exists". format(SETTINGS_PATH))
            return

        with open(SETTINGS_PATH, 'w') as f:
            f.write(Settings.as_json())
