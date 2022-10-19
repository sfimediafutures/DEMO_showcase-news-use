import json
import pandas as pd


def entries(data):
    unprocessed_data = pd.read_json(data)

    unprocessed_data = unprocessed_data.reset_index()
    unprocessed_data = unprocessed_data.rename(columns={"index":"id"})
    for i in range(unprocessed_data.__len__()):
        yield unprocessed_data.iloc[i].to_dict()
