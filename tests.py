import unittest

import checkpoint.checkpoint_function as cp

class TestExample(unittest.TestCase):
    def test_example(self):
        @cp.CheckPointFunctionDecoration
        def func(val:int):
            x = yield val,'checkpoint1'
            yield val+x,'checkpoint2'
        self.assertEqual(func(3).checkpoint2(checkpoint1=2),5)
    def test_iteration(self):
        @cp.CheckPointFunctionDecoration
        def func(val:int):
            yield val,'checkpoint1'
            yield val+1,'checkpoint2'
            yield val-10,'checkpoint3'
        
        self.assertListEqual([3,4,-7],list(func(3).checkpoint3))
    def test_iteration_if_not_declare_checkpoint(self):
        @cp.CheckPointFunctionDecoration
        def func(val:int):
            yield val,'apple'
            yield val+1,'banana'
            yield val-10,'cherry'

        self.assertListEqual([-3,-2,-13],list(func(-3)))

if __name__ == '__main__':
    unittest.main()