from urllib.request import Request
from rest_framework import serializers
from handler.models import User, Session, Entry


class SessionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = Session
        fields = ['session_id']


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    sessions = SessionSerializer(many=True)
    entries = EntrySerializer(many=True)

    class Meta:
        model = User
        fields = ['user_id']
