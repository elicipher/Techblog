from django.urls import path ,include
from . import views
from rest_framework.routers import DefaultRouter

#Article
article_router = DefaultRouter()
article_router.register(r'manager',views.ArticleManagerViewset, basename='article_manager' )
article_router.register(r'list',views.ArticleViewSet,basename='ArticleList')

#Podcast
podcast_router = DefaultRouter()
podcast_router.register(r'manager',views.PodcastManagerViewset,basename='podcast_manager')
podcast_router.register(r'episode',views.EpisodeViewset , basename='episode_manage')
podcast_router.register(r'list',views.PodcasViewset , basename='podcast_list')
urlpatterns =  [
    path('article/',include(article_router.urls)),
    path('podcast/',include(podcast_router.urls))

]

