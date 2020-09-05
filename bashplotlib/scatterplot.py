#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Plotting terminal based scatterplots
"""

from __future__ import print_function
import csv
import sys
import optparse
from .utils.helpers import *
from .utils.commandhelp import scatter


def get_scale(series, is_y=False, steps=20):
    min_val = min(series)
    max_val = max(series)
    scaled_series = []
    for x in drange(min_val, max_val, (max_val - min_val) / steps,
                    include_stop=True):
        if x > 0 and scaled_series and max(scaled_series) < 0:
            scaled_series.append(0.0)
        scaled_series.append(x)

    if is_y:
        scaled_series.reverse()
    return scaled_series


def _plot_scatter(xs, ys, size, pch, colour, title, cs, txt_align, x_title, y_title, show_axes):
    plotted = set()
    scale = len(get_scale(xs, False, size))
    x_title, y_title = "x: " + x_title, "y: " + y_title
    x_y, xp_yp = [], []
    crosses_x_axis, crosses_y_axis = max(xs) > 0 > min(xs), max(ys) > 0 > min(ys)

    if title:
        print(box_text(title, 2 * (scale + 1), txt_align))

    print(y_title)
    print("+" + "-" * (2 * scale + 2) + "+")
    for y in get_scale(ys, True, size):
        print("|", end=' ')
        for x in get_scale(xs, False, size):
            point = " "
            for (i, (xp, yp)) in enumerate(zip(xs, ys)):
                xp_yp.append((xp, yp))
                x_y.append((x, y))
                if xp <= x and yp >= y and (xp, yp) not in plotted:
                    point = pch
                    plotted.add((xp, yp))
                    if cs:
                        colour = cs[i]
                elif show_axes and y == x == 0 and (x, y) not in plotted and crosses_x_axis and crosses_y_axis :
                    point = "0"
                    plotted.add((x, y))
                    if cs:
                        colour = cs[i]
                elif show_axes and y == 0 and (x, y) not in plotted and crosses_y_axis:
                    point = "-"
                    plotted.add((x, y))
                    if cs:
                        colour = cs[i]
                elif show_axes and x == 0 and (x, y) not in plotted and crosses_x_axis:
                    point = "|"
                    plotted.add((x, y))
                    if cs:
                        colour = cs[i]
            printcolour(point + " ", True, colour)
        print(" |")
    print("+" + "-" * (2 * scale + 2) + "+")
    print(x_title.rjust((scale + 2) * 2))
    print(xp_yp)
    print(x_y)


def plot_scatter(f, xs, ys, size, pch, colour, title, x_title="My x axis", y_title="My y axis", txt_align="center", show_axes=False):
    """
    Form a complex number.

    Arguments:
        f -- comma delimited file w/ x,y coordinates
        xs -- if f not specified this is a file w/ x coordinates
        ys -- if f not specified this is a file w/ y coordinates
        size -- size of the plot
        pch -- shape of the points (any character)
        colour -- colour of the points
        title -- title of the plot
        x_title -- title of the x-coordinate of the plot
        y_title -- title of the y_coordinate of the plot
        txt_align -- alignment preference for the title of the plot
    """
    cs = None
    if f:
        if isinstance(f, str):
            with open(f) as fh:
                data = [tuple(line.strip().split(',')) for line in fh]
        else:
            data = [tuple(line.strip().split(',')) for line in f]
        xs = [float(i[0]) for i in data]
        ys = [float(i[1]) for i in data]
        if len(data[0]) > 2:
            cs = [i[2].strip() for i in data]
    elif isinstance(xs, list) and isinstance(ys, list):
        pass
    else:
        with open(xs) as fh:
            xs = [float(str(row).strip()) for row in fh]
        with open(ys) as fh:
            ys = [float(str(row).strip()) for row in fh]

    _plot_scatter(xs, ys, size, pch, colour, title, cs, txt_align, x_title, y_title, show_axes)
    

def main():
    parser = optparse.OptionParser(usage=scatter['usage'])

    parser.add_option('-f', '--file', help='a csv w/ x and y coordinates', default=None, dest='f')
    parser.add_option('-t', '--title', help='title for the chart', default="", dest='t')
    parser.add_option('-x', help='x coordinates', default=None, dest='x')
    parser.add_option('-y', help='y coordinates', default=None, dest='y')
    parser.add_option('-s', '--size', help='y coordinates', default=20, dest='size', type='int')
    parser.add_option('-p', '--pch', help='shape of point', default="x", dest='pch')
    parser.add_option('-c', '--colour', help='colour of the plot (%s)' %
                      colour_help, default='default', dest='colour')
    parser.add_option('-xt', '--x_title', help="x axis title", default="My x axis", dest="xt")
    parser.add_option('-yt', '--y_title', help="y axis title", default="My y axis", dest="yt")
    parser.add_option('-a', '--align', help='title alignment left, right \
                                           or center as strings', defaul="center", dest='alg')
    parser.add_option('h', '--axes', help='show 0-axes if values cross', default=False, dest="axs")

    opts, args = parser.parse_args()

    if opts.f is None and (opts.x is None or opts.y is None):
        opts.f = sys.stdin.readlines()

    if opts.f or (opts.x and opts.y):
        plot_scatter(opts.f, opts.x, opts.y, opts.size, opts.pch, opts.colour, opts.t, opts.xt, opts.yt, opts.alg, opts.axs)
    else:
        print("nothing to plot!")


if __name__ == "__main__":
    main()
