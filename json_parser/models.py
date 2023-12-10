from django.db import models

# Create your models here.

class Version(models.Model):
    name = models.CharField(max_length=20)
    last_digit = models.IntegerField()

class Benchmark(models.Model):
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    cpu_time = models.FloatField()