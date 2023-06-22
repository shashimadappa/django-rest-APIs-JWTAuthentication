
from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='reg'),
    path('login', views.login, name='login'),
    path('testapi', views.protected_resource, name='api'),
    path('post', views.BlogPostFunction.as_view(), name='post'),
    path('get-all', views.BlogPostGetAll.as_view(), name='get'),
    path('update/<int:pk>', views.BlogPostUpdate.as_view(), name='update'),


]
