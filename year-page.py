import os
from bs4 import BeautifulSoup
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
import pandas as pd


path = '/home/dbsm-user/data/Skripte/data/Börsenblatt/'
output_file(path + 'graph.html')

data = {}

for file in os.listdir(path):
    with open(path + file) as f:
        soup = BeautifulSoup(f, 'xml')
        try:
            data[soup.find('div', TYPE='year').get('LABEL')] =\
                len(soup.find_all('div', TYPE='page'))
        except:
            print('Shit!')
        

df = pd.DataFrame(list(data.items()), columns=['Year', 'Pages'])

print(df)

source = ColumnDataSource(df)

p = figure(title='Börsenblatt')
p.line(x='Year', y='Pages', source=source)

show(p)
