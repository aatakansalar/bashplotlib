#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Plotting terminal based histograms
"""

from __future__ import print_function
from __future__ import division

import math
from .utils.helpers import *


def calc_bins(n, min_val, max_val, h=None, binwidth=None):
    """
    Calculate number of bins for the histogram
    """
    if not h:
        h = max(10, math.log(n + 1, 2))
    if binwidth == 0:
        binwidth = 0.1
    if binwidth is None:
        binwidth = (max_val - min_val) / h
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


def plot_hist(f, width=20.0, bincount=None, binwidth=None, pch="o", colour="default", title="", ylab=None,\
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
        sd += (mean - number) ** 2
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

    if width is None:
        width = stop - start
        if width > 20:
            width = 20

    # ys is the interval values of our data ranges in the bins
    ys = list(drange(start, stop, float(stop - start) / width))

    # nlen is the size of the interval member count
    # side of the histogram that we will print at bottom
    nlen = max(len(str(min_y)), len(str(max_y))) + 1

    # We print the title with our box_text function
    if title:
        print(box_text([title], max(len(hist) * 2, len(title)), 1, "center", nlen))

    used_labs = set()

    labels = abbreviate([str(b) for b in bins])
    labels.reverse()
    x_labels_len = len(labels[0])
    for i in range(0, len(labels)):
        if labels[i] in used_labs:
            lab = ""
        else:
            used_labs.add(labels[i])
            lab = " " * (nlen - len(labels[i])) + labels[i] + "|"
        print(lab, end=" ")

        for k in range(0, len(ys)):
            if hist[i] >= int(ys[k]):
                printcolour(pch, True, colour)
            else:
                printcolour(" ", True, colour)
        print('')

    print(" " * (x_labels_len+ 1) + "+" + "-" * len(ys))
    if ylab:
        for i in range(0, nlen):
            printcolour(" " * (x_labels_len + 3), True, colour)
            for x in range(0, len(ys)):
                num = str(int(ys[x]))
                if x % 2 == 0:
                    pass
                elif i < len(num):
                    # Printing only one character of the value in each line
                    print(num[i], end=' ')
                else:
                    print(" ", end=' ')
            print('')

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


