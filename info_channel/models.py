from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post (models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Opublikowane'),
    )
    CATEGORY_CHOICES = (
        ('important_information', 'Komunikaty'),
        ('information', 'Informacje'),
        ('inner_information', 'Komunikaty firmowe'),
        ('news', 'Nowości'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=22,
                                choices=CATEGORY_CHOICES,
                                default='inner_information')
    status = models.CharField(max_length=12,
                              choices=STATUS_CHOICES,
                              default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('info_channel:post_detail', args=[self.publish.year,
                                                         self.publish.month,
                                                         self.publish.day,
                                                         self.slug])


class PostBodyParagraph(models.Model):
    IMAGE_POSITION_ChOICES = (
        ('left', 'lewa'),
        ('right', 'prawa'),
        ('center', 'centrum'),
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_body_paragraph')
    body = models.TextField()
    img_position = models.CharField(max_length=7, choices=IMAGE_POSITION_ChOICES, default='centrum')
    img_address = models.CharField(max_length=250, blank=True, null=True)
