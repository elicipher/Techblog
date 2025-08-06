from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone 
from datetime import timedelta
from .managers import UserManager 
from blog.models import Tag

# Create your models here.

class User(AbstractBaseUser):
    avatar = models.ImageField(upload_to='profile/' , null= True , blank= True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    interest = models.ManyToManyField(Tag , blank= True , related_name='interests_tags')


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name',]

    def __str__(self):
        return self.full_name
    

    objects = UserManager() #Using our manager or customized 

    def __str__(self):
        return self.email
    
    def has_perm(self , perm , obj = None):
        return True
    
    def has_module_perms(self,app_label):
        return True
    
    @property#وقتی یه متد رو با @property علامت می‌زنی، می‌تونی اون متد رو مثل یه ویژگی (attribute) صدا بزنی، نه مثل یه تابع.
    def is_staff(self):
        return self.is_admin
    
#Otpcode : one time code for login
class OtpCode(models.Model):
    email = models.EmailField(unique=True)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} - {self.code}'
    
    def check_and_delete_if_expired(self):
        return timezone.now() > self.created + timedelta(minutes=2)

      
