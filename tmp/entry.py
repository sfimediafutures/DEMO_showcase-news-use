# Bins containing lists of data, add to list if within 5 mins of last entry
import pandas as pd
import numpy as np
import re
import json
import time
from datetime import datetime

class SessionList:
    def __init__(self, head = None, tail = None, timespan = 5):
        self.head = head
        self.tail = None
        self.timespan = timespan

        self.top = self.timespan * 60000000
        self.bottom = -(self.timespan * 60000000)
    
        self.count = 0

    # takes tupe (id, usec)
    def insert(self, data):
        new_node = SessionNode(data[0], data[1])

        if not self.head:
            self.head = new_node
            self.count += 1
            print('Head')
            return True

        else:
            difference = self.head.usec - new_node.usec
            if difference < self.top and difference > self.bottom: # DIFFERENCE = 0 ?????
                self.add(new_node)
                self.count += 1

                if difference > 0:
                    self.top += difference
                else:
                    self.bottom -= difference
                return True
            else:
                return False

    def add(self, new_node):
        if self.head.usec < new_node.usec:
            self.head.set_after(new_node)
        else:
            new_node.set_after(self.head)
            self.head = new_node
        return

    def show(self):
        values = []
        item = self.head
        while item.get_after():
            values.append(item.get_data())
            item = item.get_after()
        # as while loop above will not append the tail node, we add:
        values.append(item.get_data())
        return values

class SessionNode:
    def __init__(self, item_id: int, usec: int):        
        self.id = item_id
        self.usec = usec

        self.before = None
        self.after = None

    def get_data(self):
        return (self.id, self.usec)
      
    def set_data(self, item_id, usec):
        self.id = item_id
        self.usec = usec
        
    def get_after(self):
        return self.after

    def set_after(self, after):
        self.after = after
      

    def get_before(self):
        return self.before
 
    def set_before(self, before):
        self.before = before


def run():
    data = 'cleaned_history_.json'
    unprocessed_data = pd.read_json(data)

    unprocessed_data = unprocessed_data.reset_index()
    unprocessed_data = unprocessed_data.rename(columns={"index":"id"})

    data = [(src, dst) for src, dst in zip(unprocessed_data['id'], unprocessed_data['time_usec'])]


    sessions = []
    for entry in data:
        i = 0
        # cold start
        if len(sessions) == 0:
            data_list = SessionList()
            data_list.insert(entry)
            sessions.append(data_list)
        else:
            data_list = sessions[i]
            while not data_list.insert(entry): # While im False
                i += 1
                if i + 1 > len(sessions): # End of line, create new.
                    data_list = SessionList()
                    data_list.insert(entry)
                    sessions.append(data_list)
                    break
                else:
                    data_list = sessions[i]

    for l in sessions:
        print(l.show())

if __name__ == '__main__':
    run()

