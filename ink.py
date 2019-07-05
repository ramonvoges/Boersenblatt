import os
import pandas as pd

from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
from glob import glob



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
                url = link.find('mets:FLocat')['xlink:href'])
                print("Lade herunter: {}".format(url)
                counter += 1
                file_name = "{}-{:05d}.xml".format(slub_id, counter)
                xml_download = urlopen(url)
                xml_suppe = soup(xml_download, 'xml')
                with open("/home/dbsm-user/data/Skripte/data/Börsenblatt/Einzelseiten/{}".format(file_name), 'w') as f:
                    print("Schreibe {}".format(file_name))
                    f.write(xml_suppe.prettify())
            

def load_files():
    files = '/home/dbsm-user/data/Skripte/data/Börsenblatt/Einzelseiten/*.xml'
    for xml_file in glob(files):
        with open(xml_file) as f:
            name = f.name
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

def collect_data():
    data = {'filename': [],
            'blocks': [],
            'lines': []}
    for name, xml_soup in load_files():
        data['filename'].append(name)
        data['blocks'].append(count_blocks(xml_soup))
        data['lines'].append(count_lines(xml_soup))
    return data
    
def save_data():
    data = collect_data()
    df = pd.DataFrame(data)
    df.to_csv('data.csv')
    print("Daten gesichert in: data.csv")
    #with open('data.csv', 'w') as f:
        #w = csv.DictWriter(f, data.keys())
        #w.writeheader()
        #w.writerow(data)

def load_csv():
    df = pd.read_csv('data.csv')
    return df
