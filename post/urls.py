from django.urls import path, include
from rest_framework.routers import DefaultRouter

from post import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('posts', views.PostViewSet)
router.register('images', views.ImageViewSet)

app_name = 'post'

urlpatterns = [
    path('', include(router.urls))
]

urlpatterns += [
    path('like-post/<slug:slug>', views.like_post), 
]