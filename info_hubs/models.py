from django.db import models
from django import template


register = template.Library()

class Category(models.Model):
    """The Category of an article"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        """Return a string representation of the model"""
        return self.text

class Article(models.Model):
    """The information related to an article"""
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    @register.simple_tag
    def split(self, value, delimiter):
        return value.split(delimiter)

    class Meta:
        verbose_name_plural = 'articles'

    def __str__(self):
        """Return a string representation of the model."""
        return self.text