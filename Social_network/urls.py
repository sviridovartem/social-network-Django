from django.contrib import admin
from django.urls import path
from post.views import FeedView
from sn_profile.views import frontpage, signout, profile, follows, followers, follow, stopfollow, friends

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', frontpage, name='frontpage'),
    path("feed/", FeedView.as_view(), name="feed"),
    path('signout/', signout, name='signout'),
    path('<str:username>/follows/', follows, name='follows'),
    path('<str:username>/followers/', followers, name='followers'),
    path('<str:username>/follow/', follow, name='follow'),
    path('<str:username>/friends/', friends, name='friends'),
    path('<str:username>/stopfollow/', stopfollow, name='stopfollow'),
    path('<str:username>/', profile, name='profile'),
]
