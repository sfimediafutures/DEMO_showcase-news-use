from urllib.request import Request
from rest_framework import serializers
from handler.models import User, Session, Entry


class SessionSerializer2(serializers.ModelSerializer):
    #user = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Session
        fields = ['session_id', 'user']


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'

class SessionSerializer(serializers.Serializer):
    session_id = serializers.IntegerField()
    total_time = serializers.IntegerField()
    entry = EntrySerializer(many=True)

class UserSerializer(serializers.ModelSerializer):
    session = SessionSerializer(many=True, read_only=True)
    entry = EntrySerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['user_id']

class UserSingleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id']

class CalEntrySerializer(serializers.Serializer):
    x = serializers.IntegerField()
    y = serializers.IntegerField()
    value = serializers.IntegerField()
    name = serializers.CharField()





class pieSerializer(serializers.Serializer):
        # {
            # name: 'Chrome',
            # y: 74.77,
            # sliced: true,
            # selected: true
        # }
        name = serializers.CharField()
        y = serializers.IntegerField()
        sliced = serializers.BooleanField()
        selected = serializers.BooleanField()

class DetailEntrySerializer(serializers.Serializer):
        # {
            # "n_total_articles":n_total_articles, 
            # "pie":{},
            # 'timespent':timespent, 
            # 'forside_artikkel':forside_artikkel,
        # }
    n_total_articles = serializers.IntegerField()
    pie = pieSerializer(many=True)
    timespent = serializers.CharField()
    forside_artikkel = serializers.ListField(child=serializers.IntegerField())
    sessions = serializers.ListField(child=serializers.ListField(child=serializers.FloatField()))
