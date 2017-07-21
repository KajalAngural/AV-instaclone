"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin


#importing all the functions from views.py
from myapp.views import signup_view, login_view, feed_view, post_view,like_view,comment_view

urlpatterns= [
url(r'^admin/', admin.site.urls),           #to admin page
    url('post/', post_view),            #to postview.html
    url('feed/', feed_view),            #to feed.html
    url('like/', like_view),            #to like post
    url('comment/', comment_view),          #to comment on post
    url('login1/', login_view),         #to l0gin1.html
    url('', signup_view),           #to homepage(signuo.html)


]
