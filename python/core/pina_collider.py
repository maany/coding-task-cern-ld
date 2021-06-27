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
