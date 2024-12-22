from django.urls import path,re_path
from . import views


app_name='blog_module'
urlpatterns = [
    path('',views.ArticleListView.as_view(),name="articles"),
    # article comment
    path('add-comment/article_comment/',views.add_article_comment,name='add-article-comment'),
    # article detail
    path('<int:pk>/<slug:slug>/',views.ArticleDetailView.as_view(),name="article-detail"),
    re_path(r'^(?P<pk>[0-9]+)/(?P<slug>[\w-]+)/\Z$', views.ArticleDetailView.as_view(), name='article-detail'),
]
