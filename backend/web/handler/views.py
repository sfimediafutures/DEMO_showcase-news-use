from django.shortcuts import render
from django.http import HttpResponse
from handler.models import User, Session, Entry
from handler.serializers import UserSerializer, SessionSerializer, EntrySerializer, UserSingleSerializer, CalEntrySerializer, DetailEntrySerializer

from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework import generics, pagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters


from django.http import HttpResponse, JsonResponse
from django.http import Http404
from urllib.request import urlopen

import random
import json
import requests as rq
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

class SessionPagination(pagination.PageNumberPagination):
    page_size = 40
    page_size_query_param = 'page_size'
    max_page_size = 200


# With user Id, recieve all related Sessions:
class Sessions(APIView):
    def get_sessions(self, pk): # get sessions:

        #let = Session.objects.filter(user__user_id = 88538)
        sessions = Session.objects.all().filter(user__user_id = pk)
        return sessions

        
    def get(self, request, pk, format=None, *args, **kwargs):
        # pk = userId
        # tk = recommenderId
        #tk = self.kwargs.get('pk_model', None)

        sessions = self.get_sessions(pk)

        serializer = SessionSerializer(sessions, many=True) # not finding session_id??
        return Response(serializer.data)

class Entries(APIView):
    def get_entries(self, pk): # get sessions:

        #let = Session.objects.filter(user__user_id = 88538)
        Entries = Entry.objects.all().filter(user__user_id = pk)
        return Entries

        
    def get(self, request, pk, format=None, *args, **kwargs):
        # pk = userId
        # tk = recommenderId
        #tk = self.kwargs.get('pk_model', None)

        entries = self.get_entries(pk)

        serializer = EntrySerializer(entries, many=True) # not finding session_id??
        return Response(serializer.data)

class User_Single(APIView):

    def get_users(self, pk): # get sessions:
    
        #let = Session.objects.filter(user__user_id = 88538)
        users = User.objects.all(user_id = pk)
        return users

        
    def get(self, request, pk, format=None, *args, **kwargs):
        # pk = userId
        # tk = recommenderId
        #tk = self.kwargs.get('pk_model', None)

        users = self.get_users(pk)

        serializer = UserSerializer(users, many=True) # not finding session_id??
        return Response(serializer.data)

class Users(APIView):
    def get_users(self): # get sessions:
        users = User.objects.all()
        return users

        
    def get(self, request, format=None, *args, **kwargs):
        # pk = userId
        # tk = recommenderId
        #tk = self.kwargs.get('pk_model', None)

        users = self.get_users()

        serializer = UserSingleSerializer(users, many=True) # not finding session_id??
        return Response(serializer.data)

class Month(APIView):
    def get_users(self, pk): # get sessions:
    
    #let = Session.objects.filter(user__user_id = 88538)
        users = User.objects.all(user_id = pk)
        return users

        
    def get(self, request, pk, format=None, *args, **kwargs):

        users = self.get_users(pk)

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class EntryLastMonth(APIView):

    def get_entries(self, pk):
        start_date = datetime.date(2022, 7, 20)
        end_date = datetime.date(2022, 10, 24)

        time_now = datetime.datetime.now()
        x_months_prior = time_now + relativedelta(months=-1)

        entries = Entry.objects.all().filter(user__user_id = pk, usec__gte=x_months_prior, usec__lte=time_now)
        return entries

    def get(self, request, pk, format=None, *args, **kwargs):
        entries = self.get_entries(pk)

        serializer = EntrySerializer(entries, many=True)
        return Response(serializer.data)

class EntryDateRangeUser(APIView):
    # Expects date == api/singledate/user_id/start_end
    # start_end = 'yyyy-mm-dd_yyyy-mm-dd'
    
    def get_entries(self, pk, date):
        date = date.split('_')
        start = date[0].split('-')
        end = date[1].split('-')

        start_date = datetime.date(int(start[0]), int(start[1]), int(start[2]))
        end_date = datetime.date(int(end[0]), int(end[1]), int(end[2]))

        entries = Entry.objects.all().filter(user__user_id = pk, usec__gte=start_date, usec__lte=end_date)

        return entries

    def get(self, request, pk, format=None, *args, **kwargs):
        
        date = self.kwargs.get('date', None)

        entries = self.get_entries(pk, date)

        serializer = EntrySerializer(entries, many=True) 
        return Response(serializer.data)

class EntryDateRangeUserCalFormat(APIView):
    # Expects date == api/singledate/user_id/start_end
    # start_end = 'yyyy-mm-dd_yyyy-mm-dd'
    
    def get_entries(self, pk, date):
        date = date.split('_')
        start = date[0].split('-')
        end = date[1].split('-')

        start_date = datetime.date(int(start[0]), int(start[1]), int(start[2]))
        end_date = datetime.date(int(end[0]), int(end[1]), int(end[2]))
        
        entries = Entry.objects.all().filter(user__user_id = pk, usec__gte=start_date, usec__lte=end_date)
        # Map to days
        # This should be made as an importable class.
        days = {
            "2022-09-01": [],
            "2022-09-02": [],
            "2022-09-03": [],
            "2022-09-04": [],
            "2022-09-05": [],
            "2022-09-06": [],
            "2022-09-07": [],
            "2022-09-08": [],
            "2022-09-09": [],
            "2022-09-10": [],
            "2022-09-11": [],
            "2022-09-12": [],
            "2022-09-13": [],
            "2022-09-14": [],
            "2022-09-15": [],
            "2022-09-16": [],
            "2022-09-17": [],
            "2022-09-18": [],
            "2022-09-19": [],
            "2022-09-20": [],
            "2022-09-21": [],
            "2022-09-22": [],
            "2022-09-23": [],
            "2022-09-24": [],
            "2022-09-25": [],
            "2022-09-26": [],
            "2022-09-27": [],
            "2022-09-28": [],
            "2022-09-29": [],
            "2022-09-30": [],
        }


        for entry in entries:
            days[str(entry.usec.date())].append((entry.id, entry.usec.weekday(), entry.usec.isocalendar()[1]))

        setup = []

        # self.compress in the future
        for d in days:
            if days[d] != []:
                setup.append({
                    'x':days[d][0][1],
                    'y':days[d][0][2],
                    'value': len(days[d]),
                    'name': f'Entry_{days[d][0][1]}-{days[d][0][2]}'
                })

        # x = x axis, y = y axis, value = n articles that day, name = name.
        # [{'x': 3, 'y': 35, 'value': 12, 'name': 'Entry_3-35'}, {'x': 4, 'y': 35, 'value': 3, 'name': 'Entry_4-35'}]
        return setup

    def get(self, request, pk, format=None, *args, **kwargs):
        
        date = self.kwargs.get('date', None)

        entries = self.get_entries(pk, date)
        serializer = CalEntrySerializer(entries, many=True) 
        return Response(serializer.data)

        # let formatData = [{
        #     x: 1,
        #     y: 3,
        #     value: 10,
        #     name: "Point1",
        # }, {
        #     x: 3,
        #     y: 4,
        #     value: 10,
        #     name: "Point2",
        # }]

class EntryDateUser(APIView):
    # Expects date == api/singledate/user_id/date
    # date = 'yyyy-mm-dd' OR 'weeknumber-weekday'

    #date.fromisocalendar(2020, 1, 1)  # (year, week, day of week)
    
    def get_entries(self, pk, date):
        print('YES')
        # if format 'yyyy-mm-dd'
        start = date.split('-')
        if len(date) == 3:
            start_date = datetime.date(int(start[0]), int(start[1]), int(start[2]))
        # else format wn-wd
        else:
            print('WN', date)
            start_date = datetime.date.fromisocalendar(2022, int(start[0]), int(start[1]) + 1)
            print('DATE', start_date)
            
        end_date = start_date + relativedelta(days=+1)
        print('END_DATE', end_date)

        entries = Entry.objects.all().filter(user__user_id = pk, usec__gte=start_date, usec__lt=end_date)
        return entries

    def get(self, request, pk, format=None, *args, **kwargs):
        
        date = self.kwargs.get('date', None)

        entries = self.get_entries(pk, date)

        serializer = EntrySerializer(entries, many=True) 
        return Response(serializer.data)

class DayDetailedData(APIView):

        def get_entries(self, pk, date):
            print('YES')
            # if format 'yyyy-mm-dd'
            start = date.split('-')
            if len(date) == 3:
                start_date = datetime.date(int(start[0]), int(start[1]), int(start[2]))
            # else format wn-wd
            else:
                print('WN', date)
                start_date = datetime.date.fromisocalendar(2022, int(start[0]), int(start[1]) + 1)
                print('DATE', start_date)
                
            end_date = start_date + relativedelta(days=+1)
            print('END_DATE', end_date)

            entries = Entry.objects.all().filter(user__user_id = pk, usec__gte=start_date, usec__lt=end_date)
            return entries
    
        def get_sessions(self, entries):
            
            # locate relevevant sessions:
            sessions = {}
            for e in entries:
                if e.session not in sessions.keys():
                    sessions[e.session] = 1
                else:
                    sessions[e.session] += 1

            # process all sessions
            times = []
            for session in sessions:
                if session:
                    qs = session.entry()
                    first = qs.first().usec
                    last = qs.last().usec

                    difference = ( qs.first().usec - qs.last().usec + relativedelta(minutes=5) )
                    time = [
                        float(f'{last.hour}.{int((last.minute/60)*100)}'),
                        float(f'{first.hour}.{int((first.minute/60)*100)}'),
                        [difference.hours, difference.minutes, difference.seconds]
                        ]
                    times.append(time)
                    print(time)

            return times
        
        def get(self, request, pk, format=None, *args, **kwargs):
            
            date = self.kwargs.get('date', None)

            entries = self.get_entries(pk, date)
            # len of articles
            n_total_articles = len(entries)

            sess = self.get_sessions(entries)
            # values = set(map(lambda x:x[1], mylist))
            # newlist = [[y[0] for y in mylist if y[1]==x] for x in values]
            sources = {}
            for e in entries:
                if e.source not in sources.keys():
                    sources[e.source] = 1
                else:
                    sources[e.source] += 1
            print(sources)
            print(n_total_articles)

            pie = []
            for source in sources.keys():
                pie.append({'name':source, 'y':sources[source], "sliced":True, "selected":True})
            
            print(pie)
            #  [{
            # name: 'Chrome',
            # y: 74.77,
            # sliced: true,
            # selected: true
            # },]

            # Get total timespent for a day
            timespent = '' # Her trenger vi sessions.
            hours = 0
            minutes = 0
            seconds = 0
            for s in sess:
                hours += s[2][0]
                minutes += s[2][1]
                seconds += s[2][2]

            # get seconds into minutes
            minut_sec = divmod(seconds, 60)
            minutes += minut_sec[0]
            seconds = minut_sec[1]
            
            # get minutes into seconds
            hour_minut = divmod(minutes, 60)
            hours += hour_minut[0]
            minutes = hour_minut[1]
            # Show
            timespent= f'{hours}:{minutes}:{seconds}'
            print(timespent)

            # remove timespent column:
            sess = [[y[0], y[1]] for y in sess]

            
            forside_artikkel = [0,0]
            for e in entries:
                if e.url == f'https://{e.source}/' or e.url == f'http://{e.source}/':
                    forside_artikkel[0] += 1
                else:
                    forside_artikkel[1] += 1

            print(forside_artikkel)

            # Process entries:
            return_data = {
                        "n_total_articles":n_total_articles, 
                        "pie":pie,
                        'timespent':timespent, 
                        'forside_artikkel':forside_artikkel,
                        'sessions':sess,
                        }
            serializer = DetailEntrySerializer(return_data) 
            return Response(serializer.data)


# For future addition of X and Y months, we do this manually now.
# class EntryDateXY(APIView):
    
#     def get_entries(self, pk):
#         start_date = datetime.date(2022, 7, 20)
#         end_date = datetime.date(2022, 10, 24)

#         time_now = datetime.datetime.now()
#         x_months_prior = time_now + relativedelta(months=-1)

#         entries = Entry.objects.all().filter(user__user_id = pk, usec__gte=x_months_prior, usec__lte=time_now)
#         return entries

#     def get(self, request, pk, format=None, *args, **kwargs):
#         entries = self.get_entries(pk)

#         serializer = EntrySerializer(entries, many=True) # not finding session_id??
#         return Response(serializer.data)