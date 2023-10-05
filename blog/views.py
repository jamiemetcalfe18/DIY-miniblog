from django.shortcuts import render

# Create your views here.
from django.views import generic
from .models import Blog, BlogAuthor, BlogComment
from django.contrib.auth.models import User 


def index(request):
    # index
    return render(
        request,
        'index.html',
    )
    


class BlogListView(generic.ListView): #shows blogs
    model = Blog
    paginate_by = 5

    
from django.shortcuts import get_object_or_404

class BlogListbyAuthorView(generic.ListView): #blogs by author
    model = Blog
    paginate_by = 5
    template_name ='blog/blog_list_by_author.html'
    
    def get_queryset(self):
        """
        Return list of Blog objects created by BlogAuthor (author id specified in URL)
        """
        id = self.kwargs['pk']
        target_author=get_object_or_404(BlogAuthor, pk = id)
        return Blog.objects.filter(author=target_author)
        
    def get_context_data(self, **kwargs):
        context = super(BlogListbyAuthorView, self).get_context_data(**kwargs)
        context['blogger'] = get_object_or_404(BlogAuthor, pk = self.kwargs['pk'])
        return context
    
    
class BlogDetailView(generic.DetailView):
    model = Blog

    
class BloggerListView(generic.ListView):
    model = BlogAuthor
    paginate_by = 5


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse

class BlogCommentCreate(LoginRequiredMixin, CreateView): #form for comment needs 2 be logged in
    model = BlogComment
    fields = ['description',]

    def get_context_data(self, **kwargs):
        context = super(BlogCommentCreate, self).get_context_data(**kwargs)
        context['blog'] = get_object_or_404(Blog, pk = self.kwargs['pk'])
        return context
        
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.blog=get_object_or_404(Blog, pk = self.kwargs['pk'])
        return super(BlogCommentCreate, self).form_valid(form)

    def get_success_url(self): 
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk'],})