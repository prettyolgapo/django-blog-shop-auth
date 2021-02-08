from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View

from .models import Post
from .forms import PostForm
from django.http import HttpResponse, HttpResponseRedirect
from blog.forms import ContactForm
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.db.models import Q


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    title = 'New post'
    return render(request, 'blog/post_edit.html', {'form': form, 'title': title})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    title = 'Edit post #' + pk
    return render(request, 'blog/post_edit.html', {'form': form, 'title': title})


def index(request):
    return render(request, "blog/index.html")


class ContactView(FormView):
    template_name = 'blog/contact.html'
    form_class = ContactForm
    success_url = 'thanks'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)


# def get_name(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = ContactForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             name = form.cleaned_data["name"]
#             # redirect to a new URL:
#             return redirect('blog:thanks')
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = ContactForm()
#
#     return render(request, 'blog/contact.html', {'form': form})


class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/search_results.html'

    # queryset = Post.objects.filter(name__icontains='Boston')

    def get_queryset(self):  # новый
        query = self.request.GET.get('q')
        object_list = Post.objects.filter(
            Q(title__icontains=query) | Q(text__icontains=query)
        )
        return object_list


