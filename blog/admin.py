from django.contrib import admin
from .models import Article , Tag , Podcast , Episode
# Register your models here.
admin.site.register(Tag)
admin.site.register(Podcast)
admin.site.register(Episode)
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    
    raw_id_fields = ('tag',)

