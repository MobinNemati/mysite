from django import template
from blog.models import Post, Category

register = template.Library()

@register.inclusion_tag('blog/blog-latestposts.html')
def latestposts():
    posts = Post.objects.filter(status=1).order_by('-published_date')[0:3]
    return {'posts':posts}


@register.inclusion_tag('blog/blog-category.html')
def categories():
    posts = Post.objects.filter(status=1)
    categories = Category.objects.all()
    cat_dict = {}
    for name in categories:
        cat_dict[name]=posts.filter(category=name).count()
    return {'categories':cat_dict}
