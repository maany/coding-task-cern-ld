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
        return mountain_j['left'] + (mountain_i['right'] - mountain_j['left']) / 2


def inflection_points_and_peak_tuples(mountains, pina_collider_filtered_peaks):
    inflection_map = []
    # TODO check empty
    marker_left = get_mountain_by_index(mountains, pina_collider_filtered_peaks[0])['left']
    for i, peak_idx in enumerate(pina_collider_filtered_peaks, start=0):
        if i == len(pina_collider_filtered_peaks) - 1:
            last_mountain = get_mountain_by_index(mountains, peak_idx)
            inflection_map.append((marker_left, last_mountain['right'], peak_idx))
            # TODO log breaking out of loop
            break
        next_peak_idx = pina_collider_filtered_peaks[i + 1]
        current_mountain = get_mountain_by_index(mountains, peak_idx)
        next_mountain = get_mountain_by_index(mountains, next_peak_idx)
        inflex_pt = inflection_point(current_mountain, next_mountain)
        inflection_map.append((marker_left, inflex_pt, peak_idx))
        marker_left = inflex_pt
    return inflection_map


def calculate_mountain_area(mountain, left, right):

    mountain_left = mountain['left']
    mountain_right = mountain['right']

    # move mountain to origin
    left = left - mountain_left
    right = right - mountain_left
    mountain_right = mountain_right - mountain_left
    mountain_left = 0

    # now, we can say that center of the mountain is at
    mountain_center = mountain['height']

    if right < left:
        raise Exception("Haaww")
    if right == left:
        return 0
    if right <= mountain_left or left >= mountain_right:
        return 0

    # some useful constants and lambdas:
    total_mountain_area = (mountain_right ** 2) / 4

    def _area_of_regular_right_triangle(side):
        return (side ** 2) / 2

    def _area_of_trapezium(side_vertical, side_horizonntal):
        sum_of_parallel_sides = side_vertical + (side_vertical + side_horizonntal)
        return .5 * sum_of_parallel_sides * side_horizonntal

    left_included_flag = False
    right_included_flag = False

    if left <= mountain_left:
        left_included_flag = True
        left = 0

    if right >= mountain_right:
        right_included_flag = True
        right = mountain_right

    if left_included_flag and not right_included_flag:
        if right <= mountain_center:
            return (right ** 2) / 2
        return total_mountain_area - _area_of_regular_right_triangle(mountain_right - right)

    if not left_included_flag and right_included_flag:
        if left >= mountain_center:
            return _area_of_regular_right_triangle(side=right - left)
        return total_mountain_area - _area_of_regular_right_triangle(side=left)

    if left_included_flag and right_included_flag:
        return total_mountain_area

    # if the logic reaches here, the following condition is garunteed:
    # mountain_left < left < right < mountain_right

    if left < mountain_center:
        if right <= mountain_center:
            return _area_of_trapezium(side_vertical=left, side_horizonntal=(right - left))
        return total_mountain_area - _area_of_regular_right_triangle(left) - _area_of_regular_right_triangle(
            mountain_right - right)
    return _area_of_trapezium(side_vertical=(mountain_right - right), side_horizonntal=(right-left))
