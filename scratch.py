# scratch.py
from bashplotlib.scatterplot import plot_scatter
from bashplotlib.histogram import plot_hist
from bashplotlib.horizontal_histogram import plot_hist as ph

x_coords = [-10,20,30]
y_coords = [-10,20,30]
width = 10
char = 'x'
color = 'yellow'
title = 'My Test GraphGraphGraphGraph'
align = 'center'
x_axis = 'x axis placeholder'
y_axis = 'y axis placeholder'

# plot_scatter(None, x_coords, y_coords, width, char, color, title, x_axis, y_axis, align, True)


plot_hist('exp.txt', showSummary=True, xlab=True)
print("*********************************")
ph('exp.txt', showSummary=True, ylab=True, title="Whatever")
