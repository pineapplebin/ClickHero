import pickle

data = {
    'info': {
        'id': 'mob0100100',
        'hp_curve': '%d**2 + 5',
        'money_curve': '3 * %d',
        'speed': 5
    },
    'items': [
        ('04000019_2', 15), ('04000019_1', 30), (None, 55)],
    'actions': {
        'appear': [
            {'topleft': (0, 0), 'size': (33, 23)},
            {'topleft': (33, 0), 'size': (33, 23)},
            {'topleft': (66, 0), 'size': (33, 23)},
            {'topleft': (99, 0), 'size': (33, 23)}],
        'move': [
            {'topleft': (0, 23), 'size': (33, 23)},
            {'topleft': (33, 23), 'size': (32, 23)},
            {'topleft': (65, 23), 'size': (32, 23)},
            {'topleft': (97, 23), 'size': (32, 23)},
            {'topleft': (129, 23), 'size': (33, 23)}],
        'die': [
            {'topleft': (0, 46), 'size': (39, 30)},
            {'topleft': (39, 46), 'size': (40, 30)},
            {'topleft': (79, 46), 'size': (32, 30)},
            {'topleft': (111, 46), 'size': (32, 30)},
            {'topleft': (143, 46), 'size': (31, 30)},
            {'topleft': (174, 46), 'size': (31, 30)},
            {'topleft': (205, 46), 'size': (29, 30)},
            {'topleft': (234, 46), 'size': (29, 30)},
            {'topleft': (263, 46), 'size': (29, 30)}],
    }
}


def write(filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def read(filename):
    with open(filename, 'rb') as f:
        pickle.load(f)

if __name__ == '__main__':
    write('mob0100100.pkl')
