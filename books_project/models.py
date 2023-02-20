from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=300)

    class Meta:
        verbose_name ="Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name


# to use images in github readme files 
class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    upload_date = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return str(self.upload_date)
