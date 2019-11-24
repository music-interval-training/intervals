from django.db import models

class Record(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    interval = models.CharField(max_length=30)
    guess = models.CharField(max_length=30)
    audio = models.URLField()

    @property
    def is_correct(self):
        return self.interval == self.guess 

    



