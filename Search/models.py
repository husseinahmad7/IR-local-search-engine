from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    language = models.CharField(max_length=50)

class Index(models.Model):
    term = models.CharField(max_length=255)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    frequency = models.IntegerField()
    weight = models.FloatField()
    algorithm = models.CharField(max_length=50)

    class Meta:
        indexes = [models.Index(fields=['term', 'document', 'algorithm'])]
        unique_together = ('term', 'document', 'algorithm')