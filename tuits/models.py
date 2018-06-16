from django.db import models


class Tuit(models.Model):
    tuit_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    creator = models.CharField(max_length=30)

    def __str__(self):
        return self.tuit_text.encode('utf-8').strip()


class Friendship(models.Model):
    friend1 = models.CharField(max_length=30)
    friend2 = models.CharField(max_length=30)
