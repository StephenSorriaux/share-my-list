from django.db import models
from django.contrib.auth.models import User

class Person(User):
    
    class Meta:
        proxy = True
        ordering = ('first_name', )

class List(models.Model):
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    total_cost = models.FloatField(default=0)
    pub_date = models.DateTimeField('date published', auto_now_add=True, blank=True)

    def __str__(self):
        return f"Xmas list for {self.owner}"


class Choice(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    article_text = models.CharField(max_length=255)
    link_text = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField()
    is_bought = models.BooleanField(default=False)
    is_bought_by = models.ForeignKey(Person, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.article_text