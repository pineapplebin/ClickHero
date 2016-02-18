import pickle
from util import get_file_path


class Pickle:
    def __init__(self):
        pass

    def load_map_data(self, filename):
        filename = 'map/' + filename + '.pkl'
        with open(get_file_path(filename), 'rb') as f:
            return pickle.load(f)

    def load_mob_data(self, filename):
        filename = 'mob/' + filename + '.pkl'
        data = None
        with open(get_file_path(filename), 'rb') as f:
            data = pickle.load(f)
        return data


class Database:
    def __init__(self):
        self.dbfile_name = ''
