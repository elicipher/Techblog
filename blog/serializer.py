from rest_framework import serializers
from .models import Article , Podcast , Episode

def get_tag_queryset():
    from blog.models import Tag
    return Tag.objects.all()

class RelatedArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title','cover']  


class ArticleDetailSerializer(serializers.ModelSerializer):
    related_posts  = serializers.SerializerMethodField()
    tag = serializers.PrimaryKeyRelatedField(queryset=get_tag_queryset(),many=True)
    owner = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = '__all__'

    def get_owner(self , obj):
        return obj.owner.full_name
    
    def get_related_posts(self , obj):
        tags = obj.tag.all()
        related = Article.objects.filter(tag__in = tags , status ='publish').exclude(id=obj.id).distinct()[:4]
        return RelatedArticleSerializer(related, many=True).data

class ArticleListSerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = ['id', 'title', 'owner','tag'] 

    def get_tag(self , obj):
        return [tag.slug for tag in obj.tag.all()]
    
    
    def get_owner(self , obj):
        return obj.owner.full_name

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = '__all__'
        read_only_fields  = ['created','update',]




class PodcastDetailSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    episodes = EpisodeSerializer(many=True)

    class Meta:
        model = Podcast
        fields = '__all__'
        read_only_fields  = ['publish_date',]

    def get_owner(self , obj):
        return obj.owner.full_name
    
    def create(self , validated_data):
        episodes_data = validated_data.pop('episodes', [])
        podcast = Podcast.objects.create(**validated_data)
        for ep_data in episodes_data :
            Episode.objects.create(podcast = podcast , **ep_data)

        return podcast






