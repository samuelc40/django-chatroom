from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name = 'index'),
    path('detail', views.detail, name = 'detail'),
    path('login/', views.signin, name = 'login'),
    path('register/', views.register, name = 'register'),
    path('logout', views.signout, name = 'logout'),
    path('update/', views.update_profile, name='update'),
    path('sent-friend-request/', views.sent_friend_request, name='sent-request'),
    path('accept-request/', views.accept_friend_request, name='accept-request'),
    path('f-suggest/', views.friend_suggestions, name='f-suggest'),
    path('f-request/', views.friend_request, name='f-request'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('sent_message/<int:pk>/', views.sendMessage, name='sent_message'),
    path('rec_msg/<int:pk>/', views.receiveMessage, name='rec_msg'),
    path('msg_not/', views.chatNotification, name='msg_not'),

]

