from rest_framework import viewsets 
from rest_framework.response import Response
from .models import Article
from .serializer import (
    ArticleDetailSerializer,
    ArticleListSerializer,
                         )
from .models import Article
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
        return Article.objects.filter(author = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(author = self.request.user)


    
