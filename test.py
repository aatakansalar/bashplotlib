import unittest
from bashplotlib.scatterplot import _plot_scatter


class graphTestCase(unittest.TestCase):
    def setUp(self):
        self._plot_scatter = _plot_scatter

    def tearDown(self):
        pass

    def testA(self):
        x_coords = [-10, 20, 30]
        y_coords = [-10, 20, 30]
        result = """+--------------------------+
|  My Test GraphGraphG...  |
+--------------------------+
y: y axis placeholder
+--------------------------+
|       |               x  |
|       |                  |
|       |                  |
|       |           x      |
|       |                  |
|       |                  |
|       |                  |
|       |                  |
| - - - 0 - - - - - - - -  |
|       |                  |
|       |                  |
| x     |                  |
+--------------------------+
       x: x axis placeholder"""
        assert _plot_scatter(x_coords, y_coords, 10, 'x', 'My Test GraphGraphGraphGraph', 'x axis placeholder', \
                             'y axis placeholder', 'center', True) == result, "_plot_scatter fails-cross_axis"

    def testB(self):
        x_coords = [10, 20, 30]
        y_coords = [10, 20, 30]

        result = """+--------------+
|   My Graph   |
+--------------+
y: x axis
+--------------+
|           x  |
|              |
|              |
|       x      |
|              |
| x            |
+--------------+
         x: left"""
        assert _plot_scatter(x_coords, y_coords, 5, 'x', 'My Graph', 'left', 'x axis', 'y axis', True) == \
               result, "_plot_scatter fails-simple"

    def testC(self):
        x_coords = [20, 20, 30, 15, -16, 18]
        y_coords = [20, 20, 30, 21, -35, 12]
        result = """+--------------------------+
|      My Graph Test       |
+--------------------------+
y: x axis
+--------------------------+
|         |             x  |
|         |                |
|         |       x x      |
|         |         x      |
|         |                |
| - - - - 0 - - - - - - -  |
|         |                |
|         |                |
|         |                |
|         |                |
|         |                |
| x       |                |
+--------------------------+
                    x: right"""
        assert _plot_scatter(x_coords, y_coords, 10, 'x', 'My Graph Test', 'right', 'x axis', 'y axis', True) == \
               result, "_plot_scatter fails-same_dot"


if __name__ == "__main__":
    unittest.main()
