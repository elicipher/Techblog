from rest_framework import serializers
from .models import Article

def get_tag_queryset():
    from blog.models import Tag
    return Tag.objects.all()

class RelatedArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'slug','cover']  


class ArticleDetailSerializer(serializers.ModelSerializer):
    related_posts  = serializers.SerializerMethodField()
    tag = serializers.PrimaryKeyRelatedField(queryset=get_tag_queryset(),many=True)
    author = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = '__all__'

    def get_author(self , obj):
        return obj.author.full_name
    
    def get_related_posts(self , obj):
        tags = obj.tag.all()
        related = Article.objects.filter(tag__in = tags , status ='publish').exclude(id=obj.id).distinct()[:4]
        return RelatedArticleSerializer(related, many=True).data

class ArticleListSerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'author','tag'] 

    def get_tag(self , obj):
        return [tag.slug for tag in obj.tag.all()]
    
    
    def get_author(self , obj):
        return obj.author.full_name