import os
import pandas as pd

from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
from glob import glob

import plotly.offline as py
import plotly.graph_objs as go


def download_pages():
    files = '/home/dbsm-user/data/Skripte/data/Börsenblatt/bbl-mets-data-20190703/*.mets'
    for mets in glob(files):
        print(mets)
        with open(mets) as m:
            xml = m.read()
            xml_soup = soup(xml, 'xml')
            slub_id = xml_soup.find("slub:id").string.strip()
            print(slub_id)
            counter = 0
            fulltext = xml_soup.find_all("mets:file", {'MIMETYPE': "text/xml"})
            for link in fulltext:
                url = link.find('mets:FLocat')['xlink:href']
                print("Lade herunter: {}".format(url))
                counter += 1
                file_name = "{}-{:05d}.xml".format(slub_id, counter)
                xml_download = urlopen(url)
                xml_suppe = soup(xml_download, 'xml')
                with open("/home/dbsm-user/data/Skripte/data/Börsenblatt/Einzelseiten/{}".format(file_name), 'w') as f:
                    print("Schreibe {}".format(file_name))
                    f.write(xml_suppe.prettify())
            

def load_files(year):
    files = "/home/dbsm-user/data/Skripte/data/Börsenblatt/Einzelseiten/39946221X-{}*.xml".format(year)
    for xml_file in glob(files):
        with open(xml_file) as f:
            name = os.path.basename(f.name)
            print("Lade Daten aus Datei {}".format(name))
            xml = f.read()
            xml_soup = soup(xml, 'xml')
            yield name, xml_soup

def count_blocks(xml_soup):
    blocks = xml_soup.find_all('TextBlock')
    if not blocks:
    	return 0
    else:
    	return len(blocks)

def count_lines(xml_soup):
    lines = xml_soup.find_all('TextLine')
    if not lines:
        return 0
    else:
        return len(lines)

def collect_data(year):
    data = {'filename': [],
            'blocks': [],
            'lines': []}
    for name, xml_soup in load_files(year):
        data['filename'].append(name)
        data['blocks'].append(count_blocks(xml_soup))
        data['lines'].append(count_lines(xml_soup))
    return data
    
def save_data(year):
    data = collect_data(year)
    df = pd.DataFrame(data)
    df.to_csv("data/{}.csv".format(year))
    print("Daten gesichert in: data{}.csv".format(year))
    #with open('data.csv', 'w') as f:
        #w = csv.DictWriter(f, data.keys())
        #w.writeheader()
        #w.writerow(data)

def load_csv(year):
    df = pd.read_csv("data/{}.csv".format(year))
    return df

def plot(year):
    df = load_csv(year)
    blocks = go.Bar(x=list(df['filename']), y=list(df['blocks']))
    lines = go.Bar(x=list(df['filename']), y=list(df['lines']))
    data = [blocks, lines]
    py.plot(data, filename="html/{}.html".format(year), auto_open=True)