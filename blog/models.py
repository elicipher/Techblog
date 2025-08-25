from django.db import models
from django.contrib.auth import get_user_model
import os
from django.core.validators import FileExtensionValidator
User = get_user_model()

def episode_upload_path(obj , filename):
    username = obj.podcast.owner.email
    podcast_title = obj.podcast.title.replace(" ","_")

    return os.path.join('podcasts', username, podcast_title,filename)

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name
    
class Article(models.Model):
    STATUS_CHOICE = [
        ('publish','منتشر شده'),
        ('draft','پیش نویس'),
    ]
    

    owner = models.ForeignKey(User , on_delete= models.CASCADE)
    cover = models.ImageField(upload_to='article-covers/',null=True , blank=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    tag = models.ManyToManyField(Tag , related_name='article_tag')
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICE , max_length=100)


    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title
    
    def likes_count(self):
        return self.posts_like.count()
    

    

class Like(models.Model):

    post = models.ForeignKey(Article ,on_delete=models.CASCADE , related_name='posts_like' )
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='user_likes' )

    
    def __str__(self):
        return f"{self.user} liked {self.post.title}"
    

class Podcast(models.Model):
    owner = models.ForeignKey(User ,on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='podcast-covers/')
    title = models.CharField(max_length=225)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Episode(models.Model):
    podcast = models.ForeignKey(Podcast , on_delete=models.CASCADE , related_name='episodes')
    title = models.CharField(max_length=225)
    audio_file = models.FileField(upload_to=episode_upload_path , validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'ogg'])])
    duration = models.DurationField(null= True , blank=True)
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title