import pandas as pd 
import numpy as np

from bokeh.io import show, curdoc
from bokeh.plotting import figure

from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource, Panel
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs

from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16


def make_dataset(diagnostic_df, correctness_list, range_start = 0, range_end = 3000, bin_width = 5):

    # Check to make sure the start is less than the end!
    assert range_start < range_end, "Start must be less than end!"
    
    by_correctness_df = pd.DataFrame(columns=['proportion', 'left', 'right', 
                                       'f_proportion', 'f_interval',
                                       'name', 'color'])
    range_extent = range_end - range_start
    
    # Iterate through all the carriers
    for i, correctness in enumerate(correctness_list):

        # Subset to the carrier
        subset = diagnostic_df[diagnostic_df['CORRECTNESS'] == correctness]

        # Create a histogram with specified bins and range
        arr_hist, edges = np.histogram(subset['NUM_QUESTIONS'], 
                                       bins = int(range_extent / bin_width), 
                                       range = [range_start, range_end])

        # Divide the counts by the total to get a proportion and create df
        arr_df = pd.DataFrame({'proportion': arr_hist / np.sum(arr_hist), 
                               'left': edges[:-1], 'right': edges[1:] })

        # Format the proportion 
        arr_df['f_proportion'] = ['%0.5f' % proportion for proportion in arr_df['proportion']]

        # Format the interval
        arr_df['f_interval'] = ['%d to %d minutes' % (left, right) for left, 
                                right in zip(arr_df['left'], arr_df['right'])]

        arr_df['name'] = correctness

        # Color each carrier differently
        arr_df['color'] = Category20_16[i]

        # Add to the overall dataframe
        by_correctness_df = by_correctness_df.append(arr_df)

    # Overall dataframe
    by_correctness_df = by_correctness_df.sort_values(['name', 'left'])
    
    # Convert dataframe to column data source
    return ColumnDataSource(by_correctness_df)

# Function to make the plot
def make_plot(src):
    # Blank plot with correct labels
    p = figure(plot_width = 700, plot_height = 700, 
              title = 'Histogram of Arrival Delays by Carrier',
              x_axis_label = 'Delay (min)', y_axis_label = 'Proportion')

    # Quad glyphs to create a histogram
    p.quad(source = src, bottom = 0, top = 'proportion', left = 'left', right = 'right',
           color = 'color', fill_alpha = 0.7, hover_fill_color = 'color', legend = 'name',
           hover_fill_alpha = 1.0, line_color = 'black')

    # Hover tool with vline mode
    hover = HoverTool(tooltips=[('Carrier', '@name'), 
                                ('Delay', '@f_interval'),
                                ('Proportion', '@f_proportion')],
                      mode='vline')

    p.add_tools(hover)

    p.legend.click_policy = 'hide'

    return p

if __name__ == "__main__":
  	diagnostic_df = pd.read_csv("data/daily_diagnostic_count.csv")
  	make_plot(make_dataset(diagnostic_df, [1,2,3]))

