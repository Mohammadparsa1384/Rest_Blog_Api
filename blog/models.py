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
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    
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
    name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name