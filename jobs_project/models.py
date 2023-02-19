from django.db import models


class JobCategory(models.Model):
    name = models.CharField(max_length=300)

    class Meta:
        verbose_name ="Job Category"
        verbose_name_plural = "Job Categories"

    def __str__(self):
        return self.name

