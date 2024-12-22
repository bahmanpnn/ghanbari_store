from django.shortcuts import render
from django.views import View
from django.views.generic import ListView,DetailView
from .models import Article,ArticleComment


class ArticleListView(ListView):
    template_name="blog_module/articles.html"
    model=Article
    context_object_name='articles'
    ordering=['-created_date']
    paginate_by=1


    def get_queryset(self):        
        query=super().get_queryset()
        # query=super().get_queryset().filter(is_active=True)
        
        # if self.kwargs:
        #     category=self.kwargs.get('category')
        #     if category is not None:
        #         query=query.filter(category__url_title__iexact=category,is_active=True)

        return query
    
    def get_context_data(self, **kwargs):
        '''
            if need to pass new data in product template and
            this is not product model must send with this method and override this
        '''
        context = super(ArticleListView, self).get_context_data(**kwargs)
        return context
    
    def post(self,request):
        pass


class ArticleDetailView(DetailView):
    template_name='blog_module/article_detail.html'
    model=Article
    context_object_name='article'
    
    def get_queryset(self):
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article=self.object
        comments=ArticleComment.objects.filter(parent_id=None,article_id=article.id).order_by('-created_date').prefetch_related('articlecomment_set')
        context['comments']=comments
        context['comments_count']=comments.count()
        return context

    def get_object(self, queryset = None):
        queryset=Article.objects.get(pk=self.kwargs['pk'],slug=self.kwargs['slug'])
        return queryset 


def add_article_comment(request):
    article_id=request.GET.get('article_id')
    parent_id=request.GET.get('parent_id')
    comment_text=request.GET.get('comment')
    print(article_id,parent_id,comment_text)

    new_comment=ArticleComment(parent_id=parent_id,article_id=article_id,text=comment_text,author_id=request.user.id)
    new_comment.save()

    comments=ArticleComment.objects.filter(article_id=article_id,parent_id=None).order_by('-created_date').prefetch_related('articlecomment_set')
    comments_count=ArticleComment.objects.filter(article_id=article_id).count()


    return render(request,'blog_module/includes/article_comments.html',{
        'comments':comments,
        'comments_count':comments_count
    })

