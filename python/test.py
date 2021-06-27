import unittest
from python.core.pina_collider import sort_mountains, append_index_to_mountains, get_x_axis, pina_collider as pina

class Test(unittest.TestCase):
    """
    Please specify test cases (expected behaviour of the program, according to specification)
    """
    @classmethod
    def setUpClass(cls):
        cls.mountains = [
            {'left': 9, 'right': 15, 'height': 3},
            {'left': 8, 'right': 14, 'height': 3},
            {'left': 5, 'right':  9, 'height': 2},
            {'left': 0, 'right':  6, 'height': 3},
            {'left': 2, 'right': 12, 'height': 5},
            {'left': 5, 'right': 13, 'height': 4},
        ]
        cls.indexed_mountains = [
            {'left': 9, 'right': 15, 'height': 3, 'id': 1},
            {'left': 8, 'right': 14, 'height': 3, 'id': 2},
            {'left': 5, 'right':  9, 'height': 2, 'id': 3},
            {'left': 0, 'right':  6, 'height': 3, 'id': 4},
            {'left': 2, 'right': 12, 'height': 5, 'id': 5},
            {'left': 5, 'right': 13, 'height': 4, 'id': 6},
        ]
        cls.expected_left_sorted_indexes = [4, 5, 3, 6, 2, 1]
        cls.expected_right_sorted_indexes = [4, 3, 5, 6, 2, 1]
        cls.expected_x_axis_tuples = [
            ('left', 4, 0), ('left', 5, 2), ('left', 3, 5),
            ('left', 6, 5), ('right', 4, 6), ('left', 2, 8),
            ('left', 1, 9), ('right', 3, 9), ('right', 5, 12),
            ('right', 6, 13), ('right', 2, 14), ('right', 1, 15)
        ]
        cls.expected_pina_collider_output = [4, 5, 6, 2, 1]

    def test_indexed_mountains(self):
        indexed_mountains = append_index_to_mountains(self.mountains)
        self.assertListEqual(self.indexed_mountains, indexed_mountains)
    
    def test_mountain_sorting(self):
        sorted_mountains = sort_mountains(self.indexed_mountains)
        sorted_mountain_indexes = [mountain['id'] for mountain in sorted_mountains]
        self.assertListEqual(self.expected_left_sorted_indexes, sorted_mountain_indexes)
        
        sorted_mountain_indexes = [mountain['id'] for mountain in sort_mountains(self.indexed_mountains, left_index=False)]
        self.assertListEqual(self.expected_right_sorted_indexes, sorted_mountain_indexes)

    def test_x_axis(self):
        x_axis = get_x_axis(self.indexed_mountains)
        self.assertListEqual(self.expected_x_axis_tuples, x_axis)

    def test_pina_collider(self):
        x_axis = self.expected_x_axis_tuples
        pina_collisions = pina(x_axis)
        self.assertListEqual(self.expected_pina_collider_output, pina_collisions)
