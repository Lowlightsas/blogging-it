from django.db import models
from django.contrib.auth.models import  User
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager



class Category(models.Model):
    
    category_name = models.CharField(max_length=255)
    category_slug = models.SlugField(max_length=255,unique=True)

    class Meta:
        ordering = ['category_name']
        indexes = [models.Index(fields=['category_name'])]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name
    
    def get_absolute_url(self):
        return reverse("post:post_list_by_category", args=[self.category_slug])
    

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

    
class Post(models.Model):
    
    class Status(models.TextChoices):
        DRAFT = 'DF','Draft'
        PUBLISHED = 'PB','Published'
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='posts')
    title = models.CharField(max_length=255,verbose_name='Заголовок')
    slug = models.SlugField(max_length=255,unique=True,verbose_name='URL')
    category = models.ForeignKey(Category,related_name='news',on_delete=models.CASCADE,default=1)
    body = models.TextField(verbose_name='Текст')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    status = models.CharField(max_length=2,choices=Status.choices,default=Status.DRAFT)
    published = PublishedManager()
    objects = models.Manager()
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['id','slug']),
            models.Index(fields=['title']),
            models.Index(fields=['-publish']),       
        ]
        

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.slug:
           
            self.slug = slugify(self.title)
        
        # Ensure the slug is unique
        original_slug = self.slug
        queryset = Post.objects.filter(slug=self.slug)
        count = 1
        while queryset.exists():
            self.slug = f"{original_slug}-{count}"
            queryset = Post.objects.filter(slug=self.slug)
            count += 1
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("post:detail", args=[self.id])
    
    

class PostAttachment(models.Model):
    post = models.ForeignKey(Post,related_name='attachments',on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="user/%Y/%m/%d/",blank=True)
    caption = models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return f"{self.post.title}"
    

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='author_comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created']),
            models.Index(fields=['active']),
        ]
    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()

    def __str__(self):
        return f"Message from {self.name}"
