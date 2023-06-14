from django.db import models

# Create your models here.

class Store_components(models.Model):
    logo = models.ImageField(upload_to='uploads/default', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "Site logo"
    class Meta:
        verbose_name_plural = 'Store_components'
        ordering = ('-created_at',)