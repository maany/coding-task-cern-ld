# Part 2 of the python challenge
import logging

logger = logging.getLogger(__name__)
from landscape_utils.area_algorithm import (
    sort_mountains,
    append_index_to_mountains,
    get_x_axis,
    pina_collider as pina,
    inflection_points_and_peak_tuples,
    calculate_mountain_area,
    get_mountain_by_index,
)


def visible_area(mountains):
    """ Algorithm that returns the visible area covered by the given list of mountains as float """
    indexed_mountains = append_index_to_mountains(mountains)
    x_axis = get_x_axis(indexed_mountains)
    pina_collider_filtered_peaks = pina(x_axis)
    region_to_peak_mapping = inflection_points_and_peak_tuples(
        indexed_mountains, pina_collider_filtered_peaks
    )
    total_area = 0
    for elem in region_to_peak_mapping:
        left_bound, right_bound, mountain_idx = elem
        mountain = get_mountain_by_index(indexed_mountains, mountain_idx)
        mountain_area = calculate_mountain_area(mountain, left_bound, right_bound)
        logging.debug(f"Mountain {mountain_idx}: {mountain}")
        logging.debug(
            f"Area between points {left_bound}, {right_bound}: {mountain_area}"
        )
        total_area = total_area + mountain_area
        logging.debug(f"Total Area: {total_area}")
    return total_area
