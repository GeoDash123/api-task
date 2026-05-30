from django.db import models
from django_prometheus.models import ExportModelOperationsMixin


class Dog(ExportModelOperationsMixin('dog'), models.Model):
    name = models.CharField(max_length=100, unique=True)
    breed = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)


class Task(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=100, blank=False)
    completed = models.BooleanField(default=False)
    owner = models.ForeignKey(
        "auth.User", related_name="tasks", on_delete=models.CASCADE
    )


    class Meta:
        ordering = ["created"]
