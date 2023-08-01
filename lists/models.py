from django.db import models
from django.urls import reverse

# Create your models here.
class List(models.Model):
    email = models.EmailField(max_length=70,blank=True,unique=True,default='email')
    
    def get_absolute_url(self):
        return reverse('view_list', args=[self.email])
    
    class Meta:
        ordering = ('id',)
        unique_together = ('id', 'email')

class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')
