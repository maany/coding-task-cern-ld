import unittest

from python import data_fetch
from python.landscape import Landscape
from python.landscape_utils.area_algorithm import (
    sort_mountains,
    append_index_to_mountains,
    get_x_axis,
    pina_collider as pina,
    inflection_points_and_peak_tuples,
    calculate_mountain_area,
    get_mountain_by_index,
)

from python.landscape_models.mountain import Mountain
from python.landscape_models.tree import Tree


class TestAreaAlgorithm(unittest.TestCase):
    """
    Please specify test cases (expected behaviour of the program, according to specification)
    """

    @classmethod
    def setUpClass(cls):
        cls.mountains = [
            {"left": 9, "right": 15, "height": 3},
            {"left": 8, "right": 14, "height": 3},
            {"left": 5, "right": 9, "height": 2},
            {"left": 0, "right": 6, "height": 3},
            {"left": 2, "right": 12, "height": 5},
            {"left": 5, "right": 13, "height": 4},
        ]
        cls.indexed_mountains = [
            {"left": 9, "right": 15, "height": 3, "id": 1},
            {"left": 8, "right": 14, "height": 3, "id": 2},
            {"left": 5, "right": 9, "height": 2, "id": 3},
            {"left": 0, "right": 6, "height": 3, "id": 4},
            {"left": 2, "right": 12, "height": 5, "id": 5},
            {"left": 5, "right": 13, "height": 4, "id": 6},
        ]
        cls.expected_left_sorted_indexes = [4, 5, 3, 6, 2, 1]
        cls.expected_right_sorted_indexes = [4, 3, 5, 6, 2, 1]
        cls.expected_x_axis_tuples = [
            ("left", 4, 0),
            ("left", 5, 2),
            ("left", 3, 5),
            ("left", 6, 5),
            ("right", 4, 6),
            ("left", 2, 8),
            ("left", 1, 9),
            ("right", 3, 9),
            ("right", 5, 12),
            ("right", 6, 13),
            ("right", 2, 14),
            ("right", 1, 15),
        ]
        cls.expected_pina_collider_output = [4, 5, 6, 2, 1]
        cls.expected_inflection_map = [
            (0, 4, 4),
            (4, 8.5, 5),
            (8.5, 10.5, 6),
            (10.5, 11.5, 2),
            (11.5, 15, 1),
        ]

    def test_indexed_mountains(self):
        indexed_mountains = append_index_to_mountains(self.mountains)
        self.assertListEqual(self.indexed_mountains, indexed_mountains)

    def test_mountain_sorting(self):
        sorted_mountains = sort_mountains(self.indexed_mountains)
        sorted_mountain_indexes = [mountain["id"] for mountain in sorted_mountains]
        self.assertListEqual(self.expected_left_sorted_indexes, sorted_mountain_indexes)

        sorted_mountain_indexes = [
            mountain["id"]
            for mountain in sort_mountains(self.indexed_mountains, left_index=False)
        ]
        self.assertListEqual(
            self.expected_right_sorted_indexes, sorted_mountain_indexes
        )

    def test_x_axis(self):
        x_axis = get_x_axis(self.indexed_mountains)
        self.assertListEqual(self.expected_x_axis_tuples, x_axis)

    def test_pina_collider(self):
        x_axis = self.expected_x_axis_tuples
        pina_collisions = pina(x_axis)
        self.assertListEqual(self.expected_pina_collider_output, pina_collisions)

    def test_inflection_map(self):
        region_area_map = inflection_points_and_peak_tuples(
            self.indexed_mountains, self.expected_pina_collider_output
        )
        self.assertListEqual(self.expected_inflection_map, region_area_map)

    def test_area(self):
        inflection_map = self.expected_inflection_map
        total_area = 0
        for elem in inflection_map:
            left_bound, right_bound, mountain_idx = elem
            mountain = get_mountain_by_index(self.indexed_mountains, mountain_idx)
            mountain_area = calculate_mountain_area(mountain, left_bound, right_bound)
            print(f"Mountain {mountain_idx}: {mountain}")
            print(f"Area between points {left_bound}, {right_bound}: {mountain_area}")
            total_area = total_area + mountain_area
            print(f"Total Area: {total_area}")
        self.assertEqual(total_area, 39.25)


class TestLandscapeMModelFramework(unittest.TestCase):
    def test_entity_attributes(self):
        mountain = Mountain(1)
        mountain.left = 10
        self.assertEqual(mountain.left, 10)

        self.assertEqual(mountain.left, mountain["left"])

        mountain.right = 20
        self.assertEqual(mountain.right, mountain["right"])

        mountain.left = 15
        self.assertEqual(mountain["left"], 15)
        self.assertEqual(mountain["left"], mountain.left)
        self.assertEqual(mountain._attribute_dict["left"], 15)

    def test_entity_types(self):
        mountain = Mountain(0)
        tree = Tree(1)

        self.assertTrue(mountain.is_mountain)
        self.assertTrue(tree.is_tree)
        self.assertFalse(mountain.is_tree)
        self.assertFalse(tree.is_mountain)

        self.assertEqual("Mountain", mountain.entity_type)

    def test_entity_string_repr(self):
        mountain = Mountain(2)
        mountain.left = 5
        mountain.right = 7
        mountain.altitude = 1

        expected_str_output = "ID: 2\ntype: Mountain\nleft: 5\nright: 7\naltitude: 1"
        mountain_str = str(mountain)
        self.assertEqual(expected_str_output, mountain_str)

    def test_loader_registration(self):
        self.assertEqual(2, len(Landscape.registered_loaders))

    def test_mountain_loader(self):
        pass


class TestLandscapeParsing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.URL = "https://cern.ch/sy-epc-ccs-coding-challenge/landscape"
        cls.FALLBACK_FILE = "./python/doc/example_data_set.txt"
        cls.BOGUS_URL = "asdasda"
        with open(cls.FALLBACK_FILE, encoding="utf-8") as f:
            cls.SAMPLE_DATA = f.read()

    def test_fallback_file(self):
        fallback_data = data_fetch.fetch(self.BOGUS_URL, self.FALLBACK_FILE)
        fallback_data.split("\n")
        self.assertEqual(self.SAMPLE_DATA, fallback_data)

    def test_unicode_types(self):
        mountain_as_unicode_8 = self.SAMPLE_DATA.splitlines()[0]
        tree_as_unicode_8 = self.SAMPLE_DATA.splitlines()[10]
        self.assertEqual(mountain_as_unicode_8, Mountain.unicode_8_bit)
        self.assertEqual(tree_as_unicode_8, Tree.unicode_8_bit)

    def test_loader_delegationn(self):
        landscape = Landscape()
        landscape.load(self.SAMPLE_DATA)
        for element in landscape:
            print(element)

    def test_attribute_chain_processing(self):
        pass
