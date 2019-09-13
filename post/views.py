from django.shortcuts import render
from django.views.generic.base import TemplateView

from .models import Post


def feed(request):
    userids = [id for id in request.user.sn_profile.follows.all()]
    userids.append(request.user.id)
    posts = Post.objects.filter(user_id__in=userids)[0:25]

    return render(request, 'feed.html', {'posts': posts})


class FeedView(TemplateView):
    template_name = "feed.html"

    def get(self, request, **kwargs):
        userids = [item.id for item in request.user.sn_profile.follows.all()]
        userids.append(request.user.id)
        posts = list(Post.objects.filter(user_id__in=userids)[:25])
        return self.render_to_response({
            "title": "Feed",
            "posts": posts
        })
