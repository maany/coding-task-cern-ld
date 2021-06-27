import operator


def append_index_to_mountains(mountains):
    for idx, mountain in enumerate(mountains, start=1):
        mountain["id"] = idx
    return mountains


def sort_mountains(mountains, left_index=True):
    if left_index:
        key = lambda k: k["left"]
    else:
        key = lambda k: k["right"]

    sorted_mountains = sorted(mountains, key=key)
    return sorted_mountains


def rename_key(mountain, left=False):
    if left:
        mountain["val"] = mountain.pop("left")
    else:
        mountain["val"] = mountain.pop("right")


def get_x_axis(indexed_mountains):
    left_sorted_mountains = [
        ("left", mountain["id"], mountain["left"])
        for mountain in sort_mountains(indexed_mountains, left_index=True)
    ]
    right_sorted_mountains = [
        ("right", mountain["id"], mountain["right"])
        for mountain in sort_mountains(indexed_mountains, left_index=False)
    ]
    x_axis = left_sorted_mountains + right_sorted_mountains
    x_axis.sort(key=lambda x: x[2])
    return x_axis


def pina_collider(x_axis_tuples):
    """
    peak is not awesome
    """
    open_peaks = []
    closed_peaks = []
    pina_peaks = []
    super_peak = None
    for elem in x_axis_tuples:
        orientation, idx, val = elem
        if super_peak is None:
            super_peak = idx
        if orientation == "left":
            open_peaks.append(idx)
        else:
            if idx in open_peaks:
                list.remove(open_peaks, idx)
                closed_peaks.append(idx)
                if idx == super_peak:
                    if len(open_peaks) > 0:
                        super_peak = open_peaks[0]
                    else:
                        # TODO log message
                        break
                else:
                    pina_peaks.append(idx)
            else:
                raise Exception("WTF event")
    return [x for x in closed_peaks if x not in pina_peaks]

def get_mountain_by_index(indexed_mountains, index):
    return next((mountain for mountain in indexed_mountains if mountain["id"] == index), None)

def inflection_point(mountain_i, mountain_j):
    if mountain_i['left'] >= mountain_j['left']:
        raise IndexError("WTF error happened duuudde")
    if mountain_i['right'] <= mountain_j['left']:
        return mountain_i['right']
    else:
        return mountain_i['height'] + mountain_i['left']

def inflection_points_and_peak_tuples(mountains, pina_collider_filtered_peaks):
    inflection_map = []
    # TODO check empty
    marker_left = get_mountain_by_index(mountains,pina_collider_filtered_peaks[0])['left']
    next_peak_idx = None
    next_mountain = None
    for i, peak_idx in enumerate(pina_collider_filtered_peaks, start=1):
        if i == len(pina_collider_filtered_peaks) - 1:
            last_mountain = get_mountain_by_index(mountains, peak_idx)
            inflection_map.append((marker_left, last_mountain['right'], peak_idx))
            # TODO log breaking out of loop
            break
        next_peak_idx = pina_collider_filtered_peaks[i+1]
        current_mountain = get_mountain_by_index(mountains, peak_idx)
        next_mountain = get_mountain_by_index(mountains, next_peak_idx)
        inflex_pt = inflection_point(current_mountain, next_mountain)
        inflection_map.append((marker_left, inflex_pt, peak_idx))
    return inflection_map