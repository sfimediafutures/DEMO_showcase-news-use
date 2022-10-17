import pandas as pd
import numpy as np
import re
import json
import os

# Declare input data ------------------------------------
browser_history_path = '/Users/snorrealvsvag/MediaFutures/codeprojects/showing-news-use/backend/data/Takeout/Chrome/BrowserHistory.json'
sources = '/Users/snorrealvsvag/MediaFutures/codeprojects/showing-news-use/backend/data/sources.json'
data_folder = '/Users/snorrealvsvag/MediaFutures/codeprojects/showing-news-use/backend/data/'

user = ''

# set to script path, change if wished.
output = os.getcwd()

# Internal Funcions -------------------------------------
def __add_source_url(row):
    source_url = re.sub('http\:\/\/|https\:\/\/|\/.*|\?.*|\#.*','', row.url)
    row['link'] = source_url
    return row

# Reading DataFrames ------------------------------------
browser_history = pd.read_json(browser_history_path)
links = pd.read_json(sources)

# Preparing browser history -----------------------------
browser_history = pd.json_normalize(browser_history['Browser History'])

# adding source links to validate news source up towards links dataframe
browser_history['link'] = None
browser_history = browser_history.apply(__add_source_url, axis=1)

# Make valid entries ------------------------------------
valid_entries = browser_history.merge(links, on='link')
valid_entries.to_json(f'{output}/cleaned_history_{user}.json')
print(valid_entries.head(10))
print(f'Kept {valid_entries.shape[0]} points of entires. Stored to {output}')
#links.to_json(data_folder + '/sources.json')