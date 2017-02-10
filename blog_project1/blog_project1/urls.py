"""blog_project1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from blog_app import views
from django.views import static
from django.conf import settings
from upload import upload_image

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^uploads/(?P<path>.*)$', static.serve, {'document_root':settings.MEDIA_ROOT,}),
    url(r'^admin/upload/(?P<dir_name>[^/]+)$', upload_image,name='upload_image'),
    url(r'^reg/$', views.reg, name='regist'),
    url(r'^login/$', views.do_login, name='login'),
    url(r'^logout/$', views.do_logout, name='logout'),
    url(r'^article/$',views.article,name='article'),
    url(r'^comment_post/$', views.comment_post, name='comment_post'),
    url(r'^tag_article/$', views.tag_article, name='tag_article'),
    url(r'^archive/$', views.archive, name='archive'),
    url(r'^user_detail/$', views.user_detail, name='user_detail'),
    url(r'^article_restful/$', views.ArticleListView.as_view(), name='article_restful'),
    url(r'^cate_article/$', views.cate_article, name='cate_article'),
    url(r'^article_update/(?P<id>\d+)/$', views.article_update, name='article_update'),
    url(r'^article_post/$', views.article_post, name='article_post'),

]
