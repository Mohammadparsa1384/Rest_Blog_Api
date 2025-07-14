from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    author = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="posts")
    category = models.ForeignKey('Category' ,on_delete=models.SET_NULL, null=True, related_name="posts")
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    title = models.CharField(max_length=250)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')    
    slug = models.SlugField(unique=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_date']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Category(models.Model):
<<<<<<< HEAD
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
=======
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
>>>>>>> main
    
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Tag(models.Model):
<<<<<<< HEAD
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)
=======
    name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True)
>>>>>>> main

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
<<<<<<< HEAD
        return self.name
=======
        return self.name

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)  
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)  
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_date'] 
    
    def __str__(self):
        return f'{self.content[:12]}'
>>>>>>> main
