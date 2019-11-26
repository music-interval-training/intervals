from django.db import models


class Record(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    interval = models.CharField(max_length=30)
    guess = models.CharField(max_length=30)
    audio_url = models.URLField()
    
    def __str__(self):
        return self.interval

    @property
    def is_correct(self):
        return self.interval == self.guess 

    
"""
@property decorator is just a convenient way to call the property() function, which is built in to Python.
This function returns a special descriptor object which allows direct access to the method's computed value, 
in this case, it is a boolean.
"""

