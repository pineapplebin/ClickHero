import pickle
from util import get_file_path

data = {
    'background_img': 'img/area/GrassSoil/back.png',
    'tiles_img': 'img/area/GrassSoil/tiles.png',
    'mob_id': ['mob0100100'],
    'footholds': [{
        'pos': (450, 350),
        'size': (336, 176),
        'tiles': [
            {'sub_pos': (142, 54), 'size': (26, 176)},
            {'sub_pos': [(0, 54), (71, 54)],
                'size': (71, 176), 'repeat': 4},
            {'sub_pos': (168, 54), 'size': (26, 176)}]
    }, {
        'pos': (0, 512),
        'size': (639, 176),
        'tiles': [
            {'sub_pos': [(0, 54), (71, 54)],
                'size': (71, 176), 'repeat': 9}]
    }, {
        'pos': (639, 464),
        'size': (321, 176),
        'tiles': [
            {'sub_pos': [(0, 54), (71, 54)],
                'size': (71, 176), 'repeat': 5}]
    }]
}

with open(get_file_path('map/map0001.pkl'), 'wb') as f:
    pickle.dump(data, f)
