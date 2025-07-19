from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    marks = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.strip().capitalize()
        self.subject = self.subject.strip().capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.subject}"
