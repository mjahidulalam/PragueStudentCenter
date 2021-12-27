""" Things To do:
> Get file extension name so we could filter in Detail page

"""

import os
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
# from imagekit.models import ImageSpecField 
# from imagekit.processors import  ResizeToFill, SmartResize
from django_resized import ResizedImageField
from tinymce.models import HTMLField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager
from django.shortcuts import reverse
from .utils import validate_file_extension


User = get_user_model()

class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # fullname = models.CharField(max_length=40, blank=True)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    bio = HTMLField()
    points = models.IntegerField(default=0)
    profile_pic = ResizedImageField(size=[50, 80], quality=100, upload_to="authors", default='authors/user.png', null=True)

    def __str__(self):
        return self.user.username

    @property
    def num_posts(self):
        return Post.objects.filter(user=self).count()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user)
        super(Author, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('profile',
                        args=[self.user.pk, self.user])

class CategoryDept(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    description = models.TextField(default="description")
    # approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(CategoryDept, self).save(*args, **kwargs)

    def get_url(self):
        return reverse("forum:posts", kwargs={
            "dept_id":self.id
        })
    
    def get_absolute_url(self):
        return reverse('forum:dept_filter', args=[self.id])


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    description = models.TextField(default="description")
    deptartment = models.ForeignKey(CategoryDept, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "categories"
    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def get_url(self):
        return reverse("forum:posts", kwargs={
            "slug":self.slug
        })

    def get_absolute_url(self):
        return reverse('forum:dept_filter', args=[self.id])


    @property
    def num_posts(self):
        return Post.objects.filter(categories=self).count()
    
    @property
    def last_post(self):
        return Post.objects.filter(categories=self).latest("date")


class Reply(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:100]

    class Meta:
        verbose_name_plural = "replies"


class Comment(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    replies = models.ManyToManyField(Reply, blank=True)

    def __str__(self):
        return self.content[:100]


class Post(models.Model):
    title = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = HTMLField()
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )
    tags = TaggableManager()
    comments = models.ManyToManyField(Comment, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse("forum:detail", kwargs={
            "pk" : self.pk, 
            "slug":self.slug
        })

    def get_absolute_url(self):
        return reverse('forum:list', kwargs={"pk" : self.pk, "slug" : self.slug})


    @property
    def num_comments(self):
        return self.comments.count()

    @property
    def last_reply(self):
        return self.comments.latest("date")

class UploadFiles(models.Model):
    file_upload = models.FileField(null=True, blank=True, upload_to='post_media', validators=[validate_file_extension])

    # feed_id linked to post.id 
    feed = models.ForeignKey(Post, on_delete=models.CASCADE)


    # def extension(self):
    #     file_name = os.path.basename(self.file_upload.name)
    #     split_extension = os.path.splitext(file_name)
    #     get_extension = split_extension[1]
    #     return get_extension

    def filename(self):
        return os.path.basename(self.file_upload.name)

 

    