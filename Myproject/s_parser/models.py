from django.db import models

# Create your models here.

class AllLanguages(models.Model):
    id = models.AutoField(primary_key=True)
    languageName = models.CharField(max_length=200, null=True)
    className = models.CharField(max_length=200,null=True)
    methodName = models.CharField(max_length=200,null=True)
    parameterName = models.CharField(max_length=200,null=True)
    link = models.URLField(default=0)
    score = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    etc = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.className



class BlogData(models.Model):
    title = models.CharField(max_length=200,null=True)
    link = models.URLField(null=True)

    def __str__(self):
        return self.title
