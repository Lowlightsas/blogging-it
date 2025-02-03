from django.urls import path
from django.conf import settings    
from . import views
from django.conf.urls.static import static

app_name = 'post'

urlpatterns = [
    path('',views.home,name='home'),
    path('base/',views.base,name='base'),
    path('base/<slug:category_slug>/', views.base, name='base'),
    path('create/',views.create_post,name='create_post'),
    path('<int:id>/',views.post_detail,name='detail'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),

] 
