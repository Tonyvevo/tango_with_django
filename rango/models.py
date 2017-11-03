from datetime import datetime

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Category(models.Model):

    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.views = abs(self.views)
        super(Category, self).save(*args, **kwargs)

                   
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Page(models.Model):

    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.PositiveIntegerField(default=0)
    first_visit=models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.last_visit > datetime.now():
            self.last_visit = datetime.now()
        super(Page, self).save(*args, **kwargs)
        
    
    def __str__(self):
        return self.title


class UserProfile(models.Model):
    # Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # Additional User attributes to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Return out something useful
    def __str__(self):
        return self.user.username
