import time
import csv
import socket
import json
import datetime
import random
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import *
plotly.tools.set_credentials_file(username='mac1g12', api_key='VhSOVBTQMUDQ3hqlyLRr')

plotly.tools.set_config_file(world_readable=True,
                             sharing='public')

# Make instance of stream id object 
stream_1 = go.Stream(
    token='xfto8kd7cp',  # link stream id to 'token' key
    maxpoints=80      # keep a max of 80 pts on screen
)

trace1 = go.Scatter(
  x = [],
  y = [],
  mode =  "lines + markers",
  stream = stream_1
  )

      
data = go.Data([trace1])

layout = go.Layout(title='Time Series')

# Make a figure object
fig = go.Figure(data=trace1, layout=layout)

# Send fig to Plotly, initialize streaming plot, open new tab
py.iplot(fig, filename='python-streaming')

# We will provide the stream link object the same token that's associated with the trace we wish to stream to
s = py.Stream(stream_id)

# We then open a connection
s.open()


Vref = 3.3 # ADC reference voltage
Fs = 10.0 # sample rate in Hz
ADCbits = 10.0 # bits on ADC


PORT = 33333;
HOST = '127.0.0.1'

message = {'$timestamp': str(datetime.datetime.now()), '$NO2WE': random.random(), '$NO2AE': random.random(), '$SO2WE': random.random(), '$SO2AE': random.random(), '$TEMP': random.random(), '$VREF': random.random(), '$PRES': random.random()};
message=json.dumps(message)

sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
sock.sendto(message, (HOST, PORT))

s.write(x = message["$timestamp"], y = message["$NO2WE"])

