import unittest

import checkpoint.checkpoint_function as cp

class TestExample(unittest.TestCase):
    def test_example(self):
        @cp.CheckPointFunctionDecoration
        def func(val:int):
            x = yield val,'checkpoint1'
            yield val+x,'checkpoint2'
        self.assertEqual(func(3).checkpoint2(checkpoint1=2),5)