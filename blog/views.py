from rest_framework import viewsets , filters
from rest_framework.response import Response
from .models import Article
from .serializer import (
    ArticleDetailSerializer,
    ArticleListSerializer,
    PodcastDetailSerializer,
    EpisodeSerializer,
    PodcastDetailSerializer
                         )
from .models import Article , Podcast , Episode
from permissions import IsOwnerOrReadOnly 
from rest_framework.permissions import IsAuthenticated 


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List Article + List By tag
    
    """
    
    serializer_class = ArticleListSerializer
    queryset = Article.objects.filter(status = 'publish')
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleDetailSerializer
    
    def list(self, request, *args, **kwargs):
        tag = request.query_params.get('tag_slug')
        queryset = self.queryset
        print("tag :",tag)
        print("queryset :",queryset)
        if tag:
            queryset = queryset.filter(tag__slug=tag)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

    

class ArticleManagerViewset(viewsets.ModelViewSet):
    """

    (Article Manager) for create - update - display owner posts
    
    """

    serializer_class = ArticleDetailSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated , IsOwnerOrReadOnly]
    
    def get_queryset(self):
        return Article.objects.filter(owner = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)


    
class PodcastManagerViewset(viewsets.ModelViewSet):
    """

    (Podcast Manager) for create - update - display owner posts
    
    """
  
    serializer_class = PodcastDetailSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated , IsOwnerOrReadOnly]
    def get_queryset(self):
        return Podcast.objects.filter(owner = self.request.user)
   


class EpisodeViewset(viewsets.ModelViewSet):
    """

    (episode manager) for delete and update episodes

    """
    serializer_class = EpisodeSerializer
    permission_classes = [IsAuthenticated ]
    lookup_field = 'slug'

    def get_queryset(self):
        return Episode.objects.filter(podcast__owner=self.request.user)
    
    def get_object(self):
        episode = super().get_object()
        if episode.podcast.owner != self.request.user:
            raise PermissionDenied("you have't permission to edit this episode")
        return episode


class PodcasViewset(viewsets.ReadOnlyModelViewSet):
    """
    
    List Podcast Public

    """
    serializer_class = PodcastDetailSerializer
    lookup_field = 'slug'
    queryset = Podcast.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['owner__full_name','title']




