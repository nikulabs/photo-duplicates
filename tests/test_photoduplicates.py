import unittest
from parameterized import parameterized

import phototool


class PhotoDuplicates(unittest.TestCase):
    
    @parameterized.expand([
        [[1,2,3,10], [[1,2,3],[10]]]
    ])
    def test_find_duplicates(self, input, exp_output):
        hashes = {k:[None] for k in input}
        exp_groups = {tuple(k):[None]*len(k) for k in exp_output}
        actual_groups = phototool.find_duplicates(hashes)
        self.assertDictEqual(exp_groups, actual_groups)


if __name__ == '__main__':
    unittest.main()