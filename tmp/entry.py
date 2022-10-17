# Bins containing lists of data, add to list if within 5 mins of last entry
import pandas as pd
import numpy as np
import re
import json
import time

class SessionString:
    def __init__(self, item_id: int, usec: int, timespan = 5):
        self.id = item_id
        self.usec = usec
        self.timespan = timespan

        self.top = self.timespan * 60000000
        self.bottom = -(self.timespan * 60000000)

        # data sctructure points
        self.before = None
        self.after = None
        

    # This will always be called on head, which is the first object timewise
    def add(self, new_entry: object):
        difference = self.usec - new_entry.usec
        if difference < self.top and difference > self.bottom:
            print(show_time(a))
            print(show_time(b))
            print(f'Within {self.timespan} mins!')
            self.place(new_entry, difference)
            return True
        else:
            print(show_time(a))
            print(show_time(b))
            print('Not Within mins!', difference / 60000000, 'minutes apart.')
            return False


    def place(self, new_entry: object, difference: int):
        head = self
        # if difference is less than 0, set new head.
        if difference < 0:
            # add 
            head.before = new_entry
            new_entry.after = head
            # add difference to bottom (maximum allowed time)
            new_entry.bottom = head.bottom - difference
            self = new_entry

        # if difference is positive, we will not replace head, but we will add to tail.
        else:
            item = head
            before = None
            # go to after untill either item is null (we reached tail)
            # or fix after.
            while item.after:

                if item.usec < new_entry.usec:
                    # if we're at tail:
                    item = item.after
                
                else: 
                    # place
                    before = item.before

                    new_entry.before = before
                    before.after = new_entry
                    new_entry.after = item
                    item.before = new_entry
                    break
            
            # if while loop ran out due to no after:
            if not item.after:
                head.bottom += difference
                item.after = new_entry
                new_entry.before = item

    def as_list(self):
        values = []
        # go to first item
        head = self.get_head()
        
        # iterate and grab all entries
        while head.after:
            values.append((head.id, head.usec))
            head = head.after

        return values
        
    def get_head(self):
        head = self
        while head.before:
            head = head.before
        return head
