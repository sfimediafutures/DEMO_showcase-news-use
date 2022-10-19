from django.db import models

# Create your models here.


class User(models.Model):
    user_id = models.IntegerField()


class Session(models.Model):
    session_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Entry(models.Model):
    entry_id = models.IntegerField()
    favicon = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    usec = models.DateTimeField(auto_now=False, auto_now_add=False)
    page_transition = models.CharField(max_length=50)
    client_id = models.CharField(max_length=100)
    source = models.CharField(max_length=100)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)


