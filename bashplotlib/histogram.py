#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Plotting terminal based histograms
"""

from __future__ import print_function
from __future__ import division

import os
import sys
import math
import optparse
from os.path import dirname
from .utils.helpers import *
from .utils.commandhelp import hist


def calc_bins(n, min_val, max_val, h=None, binwidth=None):
    """
    Calculate number of bins for the histogram
    """

    # This process is just calculating how many variables fall
    # on certain intervals
    if not h:
        h = max(10, math.log(n + 1, 2))
    # Calculating the size of the intervals
    if binwidth == 0:
        binwidth = 0.1
    if binwidth is None:
        binwidth = (max_val - min_val) / h
    # Calculating the intervals with previously calculate interval size
    # In our data's range (min, max)
    for b in drange(min_val, max_val, step=binwidth, include_stop=True):
        if b.is_integer():
            yield int(b)
        else:
            yield b


def read_numbers(numbers):
    """
    Read the input data in the most optimal way
    """
    if isiterable(numbers):
        for number in numbers:
            yield float(str(number).strip())
    else:
        with open(numbers) as fh:
            for number in fh:
                yield float(number.strip())


def run_demo():
    """
    Run a demonstration
    """
    module_dir = dirname(dirname(os.path.realpath(__file__)))
    demo_file = os.path.join(module_dir, 'examples/data/exp.txt')

    if not os.path.isfile(demo_file):
        sys.stderr.write("demo input file not found!\n")
        sys.stderr.write("run the downloaddata.sh script in the example first\n")
        sys.exit(1)

    # plotting a histogram
    print("plotting a basic histogram")
    print("plot_hist('%s')" % demo_file)
    print("hist -f %s" % demo_file)
    print("cat %s | hist" % demo_file)
    plot_hist(demo_file)
    print("*" * 80)

    # with colours
    print("histogram with colours")
    print("plot_hist('%s', colour='blue')" % demo_file)
    print("hist -f %s -c blue" % demo_file)
    plot_hist(demo_file, colour='blue')
    print("*" * 80)

    # changing the shape of the point
    print("changing the shape of the bars")
    print("plot_hist('%s', pch='.')" % demo_file)
    print("hist -f %s -p ." % demo_file)
    plot_hist(demo_file, pch='.')
    print("*" * 80)

    # changing the size of the plot
    print("changing the size of the plot")
    print("plot_hist('%s', height=35.0, bincount=40)" % demo_file)
    print("hist -f %s -s 35.0 -b 40" % demo_file)
    plot_hist(demo_file, height=35.0, bincount=40)


def plot_hist(f, height=20.0, bincount=None, binwidth=None, pch="o", colour="default", title="", xlab=None,\
            showSummary=False, regular=False, x_title="x_axis", y_title="y_axis"):
    """
    Make a histogram

    Arguments:
        height -- the height of the histogram in # of lines
        bincount -- number of bins in the histogram
        binwidth -- width of bins in the histogram
        pch -- shape of the bars in the plot
        colour -- colour of the bars in the terminal
        title -- title at the top of the plot
        xlab -- boolen value for whether or not to display x-axis labels
        showSummary -- boolean value for whether or not to display a summary
        regular -- boolean value for whether or not to start y-labels at 0
    """
    # We set our graph character
    if pch is None:
        pch = "o"

    # If the user's file input is the name, we open the file and read it to f
    if isinstance(f, str):
        with open(f) as fh:
            f = fh.readlines()


    # n is the number of numbers in our data. We find the max and min
    # values, and calculate the mean avg of our data here.

    # Read number is our method that helps us to get numbers from our file
    # And makes them iterables if they are not already

    min_val, max_val = None, None
    n, mean, sd = 0.0, 0.0, 0.0
    for number in read_numbers(f):
        n += 1
        if min_val is None or number < min_val:
            min_val = number
        if max_val is None or number > max_val:
            max_val = number
        mean += number

    mean /= n

    # We are calculating the standard deviation, which is basically just
    # how far away from the mean avg the number is. This is the
    # implementation of the whole formula. We just calculate it to
    # print in the summary part
    for number in read_numbers(f):
        sd += (mean - number)**2

    sd /= (n - 1)
    sd **= 0.5

    # Calculating the bins for our graph. What are bins? Intervals of
    # our data range. We will count how many elements fall on each interval
    # and use those counts to print our graph. (sütunlar için)
    bins = list(calc_bins(n, min_val, max_val, bincount, binwidth))

    # We store our interval values in a dictionary. Keys our interval values.
    # Items will be the number of elements in an interval
    hist = dict((i, 0) for i in range(len(bins)))

    # Calculating the number of elements on each interval and storing
    # the data on our dictionary object
    for number in read_numbers(f):
        for i, b in enumerate(bins):
            if number <= b:
                hist[i] += 1
                break
        if number == max_val and max_val > bins[len(bins) - 1]:
            hist[len(hist) - 1] += 1

    # Getting the min and max of our dictionary items. This value is
    # The left side of the histogram: how many items are in a bin?
    min_y, max_y = min(hist.values()), max(hist.values())

    # Calculating the start and stop values for drange function
    # Which will calculate the interval values again, this time not
    # for our data but the number of data in the intervals, so the
    # left side of our histogram
    start = max(min_y, 1)
    stop = max_y + 1

    if regular:
        start = 1

    if height is None:
        height = stop - start
        if height > 20:
            height = 20

    # ys is the interval values of our data ranges in the bins
    ys = list(drange(start, stop, float(stop - start) / height))
    ys.reverse()

    # nlen is the size of the left side of the histogram that we will print
    nlen = max(len(str(min_y)), len(str(max_y))) + 1

    # We print the title with our box_text function
    if title:
        print(box_text([title], max(len(hist) * 2, len(title)), 1, "center", nlen))

    # Printing the y axis title
    print(y_title)

    # To print a interval value label only once, we print it only once
    used_labs = set()
    for y in ys:
        # Turn the interval value to a string
        ylab = str(int(y))
        # Check if it is already printed
        if ylab in used_labs:
            ylab = ""
        else:
            used_labs.add(ylab)
            # Modify ylab string however we like
            ylab = " " * (nlen - len(ylab)) + ylab + "|"

        # Print the interval value
        print(ylab, end=' ')

        # Our loop looks at every interval value in our dictionary
        for i in range(len(hist)):
            # if the number of items in that interval is greater
            # than the y values interval, that means in that interval
            # there is values. so we print it. If not, we print an empty
            # character.
            if int(y) <= hist[i]:
                printcolour(pch, True, colour)
            else:
                printcolour(" ", True, colour)
        print('')


    xs = hist.keys()
    # Print the "-" character at the bottom of the histogram
    # The number of characters is the number of keys in our hist dictionary
    print(" " * (nlen + 1) + "-" * len(xs))

    # If user wanted x labels to be printed
    if xlab:
        # Abbreviate takes a list of strings, and returns a shortened,
        # equal length strings to print
        labels = abbreviate([str(b) for b in bins])
        xlen = len(labels[0])
        # We print xlen number of lines
        for i in range(0, xlen):
            # Offset
            printcolour(" " * (nlen + 1), True, colour)
            # What we print is the shortened interval values in hist
            # dictionary. We print the value of each
            for x in range(0, len(hist)):
                num = labels[x]
                # Only printing at even points to separate them
                if x % 2 != 0:
                    pass
                elif i < len(num):
                    # Printing only one character of the value in each line
                    print(num[i], end=' ')
                else:
                    print(" ", end=' ')
            # for next line
            print('')

    print(x_title.rjust(len(hist)*2))
    center = max(map(len, map(str, [n, min_val, mean, max_val])))
    center += 15

    # Printing the summary with box text helper function
    if showSummary:
        summary_lines = [
            "Summary",
            "observations: %d" % n,
            "min value: %f" % min_val,
            "mean : %f" % mean,
            "std dev : %f" % sd,
            ("max value: %f" % max_val)
        ]
        print(box_text(summary_lines, max(len(hist) * 2, len(title)), 2, "center", nlen))

def main():

    parser = optparse.OptionParser(usage=hist['usage'])

    parser.add_option(
        '-f', '--file', help='a file containing a column of numbers', default=None, dest='f')
    parser.add_option('-t', '--title', help='title for the chart', default="", dest='t')
    parser.add_option(
        '-b', '--bins', help='number of bins in the histogram', type='int', default=None, dest='b')
    parser.add_option('-w', '--binwidth', help='width of bins in the histogram',
                      type='float', default=None, dest='binwidth')
    parser.add_option('-s', '--height', help='height of the histogram (in lines)',
                      type='int', default=None, dest='h')
    parser.add_option('-p', '--pch', help='shape of each bar', default='o', dest='p')
    parser.add_option('-x', '--xlab', help='label bins on x-axis',
                      default=None, action="store_true", dest='x')
    parser.add_option('-c', '--colour', help='colour of the plot (%s)' %
                      colour_help, default='default', dest='colour')
    parser.add_option('-d', '--demo', help='run demos', action='store_true', dest='demo')
    parser.add_option('-n', '--nosummary', help='hide summary',
                      action='store_false', dest='showSummary', default=True)
    parser.add_option('-r', '--regular',
                      help='use regular y-scale (0 - maximum y value), instead of truncated y-scale (minimum y-value - maximum y-value)',
                      default=False, action="store_true", dest='regular')

    opts, args = parser.parse_args()

    if opts.f is None:
        if len(args) > 0:
            opts.f = args[0]
        elif opts.demo is None or opts.demo is False:
            opts.f = sys.stdin.readlines()

    if opts.demo:
        run_demo()
    elif opts.f:
        plot_hist(opts.f, opts.h, opts.b, opts.binwidth, opts.p, opts.colour,
                  opts.t, opts.x, opts.showSummary, opts.regular)
    else:
        print("nothing to plot!")


if __name__ == "__main__":
    main()
