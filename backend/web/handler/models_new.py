from django.db import models

# Create your models here.


class User(models.Model):
    user_id = models.IntegerField()
    session = models.ManyToManyField("handler.Session")

class Session(models.Model):
    session_id = models.IntegerField()
    user = models.models.ManyToManyField("handler.User")


class Entry(models.Model):
    entry_id = models.BigIntegerField()
    favicon = models.CharField(max_length=200, null=True)
    url = models.URLField(max_length=500)
    usec = models.DateTimeField(auto_now=False, auto_now_add=False)
    page_transition = models.CharField(max_length=50)
    client_id = models.CharField(max_length=100)
    source = models.CharField(max_length=100)


    user = models.ManyToManyField("handler.User")
    session = models.ManyToManyField("handler.Session", null=True)


