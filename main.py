# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

# Each tab is drawn by one script
from scripts.bokeh0 import bokeh0
from scripts.bokeh1 import bokeh1

# Using included state data from Bokeh for map
from bokeh.sampledata.us_states import data as states

# Create each of the tabs
tab1 = bokeh0()
tab2 = bokeh1()

# Put all the tabs into one application
tabs = Tabs(tabs = [tab1, tab2])

# Put the tabs in the current document for display
curdoc().add_root(tabs)