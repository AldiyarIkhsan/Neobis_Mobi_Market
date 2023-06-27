from django.db import models
from authentication.models import User

class Product(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    short_description = models.CharField(max_length=150)
    detailed_description = models.TextField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.username