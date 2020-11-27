from django.urls import path
from .views import *


urlpatterns = [
    path('collection/', collection, name='collection'),
    path('collection/<str:uuid>/', collection, name='collection'),
    path('movies/', collection_home, name='movies'),
    path('register/', login_view, name='register'),
    path('request-count/', server_hit_count, name='request-count'),
    path('reset/', server_hit_reset_count, name='reset'),
]
