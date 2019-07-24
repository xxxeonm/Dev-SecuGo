from django.db import models


class Data(models.Model):
    seq = models.IntegerField(primary_key=True,blank=True)
    keywords = models.CharField(max_length=128,null=True,blank=True)
    entities = models.CharField(max_length=128,null=True,blank=True)
    categories = models.CharField(max_length=255, null=True,blank=True)
    desc = models.TextField(null=True,blank=True)
    source = models.CharField(max_length=128,null=True,blank=True)
    check = models.TextField(null=True,blank=True)
    etc = models.CharField(max_length=128,null=True,blank=True)

    def __str__(self):
        return self.keywords

class CompareSource(models.Model):
    java = models.TextField(null=True, blank=True)
    class Meta:
        app_label='compareSource'