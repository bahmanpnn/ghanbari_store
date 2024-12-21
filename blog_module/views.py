from django.shortcuts import render
from django.views import View
from django.views.generic import ListView,DetailView
from .models import Article


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
        return context

    def get_object(self, queryset = None):
        queryset=Article.objects.get(pk=self.kwargs['pk'],slug=self.kwargs['slug'])
        return queryset 

