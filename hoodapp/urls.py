from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path('',views.index,name='Index'),
    path('logout', views.logout, name='logout'),
    path('new/profile/',views.new_profile, name='profile'),
    path('all-hoods/',views.neighbourhoods,name='neighbourhood'),
    path('new-hood/', views.create_neighbourhood, name='new-hood'),
    path('join_hood/<id>', views.join_neighbourhood, name='join-hood'),
    path('leave_hood/<id>', views.leave_neighbourhood, name='leave-hood'),
    path('single_hood/<hood_id>', views.single_neighbourhood, name='single-hood'),
    path('<hood_id>/post/', views.create_post, name='post'),
    path('search/', views.search_business, name='search'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root = settings.MEDIA_ROOT
    )


