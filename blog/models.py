from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
class Article(models.Model):
    STATUS_CHOICE = [
        ('publish','منتشر شده'),
        ('draft','پیش نویس'),
    ]
    

    author = models.ForeignKey(User , on_delete= models.CASCADE)
    cover = models.ImageField(upload_to='article-covers/',null=True , blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
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