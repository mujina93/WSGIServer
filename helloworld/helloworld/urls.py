from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'helloworld.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    path('admin/', admin.site.urls),
    path('hello', views.index),
]
