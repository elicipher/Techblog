from django.urls import path ,include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'manager/',views.ArticleManagerViewset, basename='article_manager' )
router.register(r'list',views.ArticleViewSet,basename='ArticleList')
urlpatterns =  [
    path('article/',include(router.urls)),

]

