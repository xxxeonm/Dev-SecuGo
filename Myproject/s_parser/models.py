from django.db import models

# Create your models here.

class AllLanguages(models.Model):
    languageName = models.CharField(max_length=200) #primary_key=True,blank=True,
    className = models.CharField(max_length=200)
    methodName = models.CharField(max_length=200)
    parameterName = models.CharField(max_length=200)
    link = models.URLField(default=0)
    score = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    etc = models.CharField(max_length=200)

    def __str__(self):
        return self.className



class BlogData(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField()

    def __str__(self):
        return self.title
