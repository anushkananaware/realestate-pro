from django.urls import path
from . import views
urlpatterns = [
    path('analyze/', views.analyze, name='analyze'),
    path('compare/', views.compare, name='compare'),
    path('upload/', views.upload_dataset, name='upload_dataset'),
    path('download/', views.download_filtered, name='download_filtered'),
]
