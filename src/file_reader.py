import json
from typing import List
import os.path
from data_object import DataObject
from exception import error


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
