def append_index_to_mountains(mountains):
    for idx, mountain in enumerate(mountains, start=1):
        mountain['id'] = idx
    return mountains

def sort_mountains(mountains, left_index = True):
    if left_index:
        key = lambda k: k['left']
    else:
        key = lambda k: k['right']

    sorted_mountains = sorted(mountains, key=key)
    return sorted_mountains

def get_mountains_on_x_axis(mountains):
    pass