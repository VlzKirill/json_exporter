from django.db import models

# Create your models here.

class BenchmarkData(models.Model):
    version_value = models.IntegerField()
    benchmark_name = models.CharField(max_length=255)
    real_time = models.FloatField()