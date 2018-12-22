from bokeh.plotting import figure
from bokeh.models import Panel
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool

import pandas as pd 
import numpy as np

from os.path import dirname, join

def bokeh1():
    df = pd.read_csv(join(dirname(dirname(__file__)), 'data', 'daily_diagnostic_count.csv'))

    arr_hist, edges = np.histogram(df[df.CORRECTNESS == 1]['NUM_QUESTIONS'], bins = 50)


    correct_question = pd.DataFrame({'question_count': arr_hist, 'left': edges[:-1], \
                       			  'right': edges[1:]})

    src = ColumnDataSource(correct_question)
    src.data.keys()

    correct_question['f_interval'] = ['%d to %d minutes' % (left, right) for left, right in zip(correct_question['left'], correct_question['right'])]

    p = figure(
        plot_height = 600,
        plot_width = 600, 
        title = 'Histogram of Number of Correct Diagnostic Questions',
        x_axis_label = 'Number of Questions', 
        y_axis_label = 'Count')

    # Add a quad glyph
    p.quad(
        source = src,
        bottom=0,
        top='question_count', 
        left='left',
        right='right', 
        fill_color='red',
        line_color='black',
        hover_fill_color = 'navy')

    h = HoverTool(tooltips = [('Interval Left', '@left'), ('(x,y)', '($x, $y)')])

    p.add_tools(h)

    tab = Panel(child = p, title = 'bokeh1')

    return tab