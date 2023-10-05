from django.db import models

# Create your models here.

from datetime import date
from django.urls import reverse #make url by reverse pattern
from django.contrib.auth.models import User #author or commentor


class BlogAuthor(models.Model): #a blogger
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    bio = models.TextField(max_length=400, help_text="Enter your bio details here.")
    
    class Meta:
        ordering = ["user","bio"]

    def get_absolute_url(self):

        return reverse('blogs-by-author', args=[str(self.id)])

    def __str__(self):
        return self.user.username


class Blog(models.Model): #blogpost
    name = models.CharField(max_length=200)
    author = models.ForeignKey(BlogAuthor, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=2000, help_text="Enter you blog text here.")
    post_date = models.DateField(default=date.today)
    
    class Meta:
        ordering = ["-post_date"]
    
    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

class BlogComment(models.Model): #comments on blog
    description = models.TextField(max_length=1000, help_text="Enter comment about blog here.")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post_date = models.DateTimeField(auto_now_add=True)
    blog= models.ForeignKey(Blog, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ["post_date"]

    def __str__(self):
        len_title=75
        if len(self.description)>len_title:
            titlestring=self.description[:len_title] + '...'
        else:
            titlestring=self.description
        return titlestring