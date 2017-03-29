# this client is taking data from the csv file outputted by client and plots it to plotly every few seconds

import plotly
import plotly.plotly as py
from plotly.graph_objs import *
plotly.tools.set_credentials_file(username='mac1g12', api_key='VhSOVBTQMUDQ3hqlyLRr')

plotly.tools.set_config_file(world_readable=True,
                             sharing='public')

data = Data([ Scatter(x=[1, 2], y=[3, 4]) ])

plot_url = py.plot(data, filename='my plot')
