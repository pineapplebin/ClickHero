import os
from random import randint


def get_file_path(filepath):
    root_path = os.path.dirname(os.path.dirname(__file__))
    l = filepath.split('/')
    filename, dirlist = l[-1], l[:-1]
    for d in reversed(dirlist):
        filename = os.path.join(d, filename)
    return os.path.join(root_path, os.path.join('resources', filename))


def randindex(length):
    return int(randint(0, 100) % length)


def check_chance(percentage):
    return randint(0, 100) <= percentage
