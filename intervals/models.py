from django.db import models


class Record(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    interval = models.CharField(max_length=30)
    guess = models.CharField(max_length=30)
    audio_url = models.URLField()
    is_correct = models.IntegerField(default=0)
    def __str__(self):
        return self.interval
    def save(self, *args, **kwargs):
        if self.interval == self.guess:
            self.is_correct = 1
        super().save(*args, **kwargs)
