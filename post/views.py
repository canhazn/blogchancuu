from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views import generic
from .models import Post, Tag

from .forms import CommentForm


def postList(request):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    # tags = Post  .tag.all()

    return render(request, 'index.html', {
        'posts': queryset,
        # 'tags': tags
    })

# class PostDetail(generic.DetailView):
#     model = Post
#     template_name = 'postDetail.html'

def postDetail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted

    print(post.title)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            return redirect("/" + str(post.slug))
    else:
        comment_form = CommentForm()

    print(request.POST)
    return render(request, template_name, {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': CommentForm()
    })

def tagDetail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = tag.post_set.all()
    context = {
        'tag': tag,
        'posts': posts
    }
    return render(request, 'tag_detail.html', context)