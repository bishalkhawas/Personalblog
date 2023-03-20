from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from blog_app.models import Post
from blog_app.forms import PostForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.generic import ListView,DetailView,DeleteView,CreateView,View
from django.contrib.auth.mixins import LoginRequiredMixin

class PostListView(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(published_at__isnull=False).order_by("-published_at")
# def post_list(request):
#     posts = Post.objects.filter(published_at__isnull=False).order_by("-published_at")
#     return render(
#         request,
#         "post_list.html",
#         {"posts": posts},
#     )

class DraftListView(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(published_at__isnull=True).order_by("-published_at")
# @login_required
# def draft_list(request):
#     posts = Post.objects.filter(published_at__isnull=True).order_by("-published_at")
#     return render(
#         request,
#         "post_list.html",
#         {"posts": posts},
#     )

class PostDetailView(DetailView):
    model = "Post"
    template_name = "post_detail.html"
    context_object_name = "post"
# def post_detail(request, pk):
#     # post = Post.objects.get(pk=pk)
#     post = get_object_or_404(Post, pk=pk)
#     return render(
#         request,
#         "post_detail.html",
#         {"post": post},
#     )

class PostDeleteView(DeleteView):
    model = "Post"
    success_url = reverse_lazy("post-list")
    def form_valid(self, form):
        messages.success(self.request, "Post was successfully deleted")
        return super().form_valid(form)

# @login_required
# def post_delete(request, pk):
#     # post = Post.objects.get(pk=pk)
#     post = get_object_or_404(Post, pk=pk)
#     post.delete()
#     messages.success(request, "Post was successfully deleted")
#     return redirect("post-list")

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "post_create.html"
    success_url = reverse_lazy
# @login_required
# def post_create(request):
#     form = PostForm()
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             messages.success(request, "Post was successfully created")
#             return redirect("post-list")
#         else:
#             messages.error(request, "Post was not created")

#     return render(
#         request,
#         "post_create.html",
#         {"form": form},
#     )

class PostPublishView(LoginRequiredMixin, View):
    def get(self, request,  pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        post.published_at = timezone.now()
        post.save()
        messages.success(request, "Post was successfully published")
        return redirect("post-list")
# @login_required
# def post_publish(request, pk):
#     # post = Post.objects.get(pk=pk)
#     post = get_object_or_404(Post, pk=pk)
#     post.published_at = timezone.now()
#     post.save()
#     messages.success(request, "Post was successfully published")
#     return redirect("post-list")


@login_required
def post_update(request, pk):
    # post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(instance=post)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post was successfully updated")
            return redirect("post-list")
        else:
            messages.error(request, "Post was not updated")
    return render(request, "post_create.html", {"form": form})


def handeler404(request, exception, template_name="404.html"):
    return render(request, template_name, status=404)
