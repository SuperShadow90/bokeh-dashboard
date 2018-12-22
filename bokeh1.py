from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool
import pandas as pd 
import numpy as np

df = pd.read_csv("data/daily_diagnostic_count.csv")

arr_hist, edges = np.histogram(df[df.CORRECTNESS == 1]['NUM_QUESTIONS'], bins = 50)


correct_question = pd.DataFrame({'question_count': arr_hist, 'left': edges[:-1], \
                       			  'right': edges[1:]})

src = ColumnDataSource(correct_question)
src.data.keys()

correct_question['f_interval'] = ['%d to %d minutes' % (left, right) for left, right in zip(correct_question['left'], correct_question['right'])]

output_file("visualization/test_histogram.html")

p = figure(plot_height = 600, plot_width = 600, 
           title = 'Histogram of Number of Correct Diagnostic Questions',
           x_axis_label = 'Number of Questions', 
           y_axis_label = 'Count')

# Add a quad glyph
p.quad(source = src, bottom=0, top='question_count', 
       left='left', right='right', 
       fill_color='red', line_color='black', hover_fill_color = 'navy')

h = HoverTool(tooltips = [('Interval Left', '@left'),
                          ('(x,y)', '($x, $y)')])


p.add_tools(h)

# Show the plot
show(p)