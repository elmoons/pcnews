from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from .models import Articles
from .forms import ArticlesForm
from django.views.generic import DetailView, UpdateView, DeleteView
from django.db.models import Q


def news_home(request):
    if 'q' in request.GET:
        q = request.GET['q']
        news = Articles.objects.filter(Q(title__icontains=q) | Q(full_text__icontains=q))
    else:
        news = Articles.objects.order_by('-date')
    return render(request, 'news/news_home.html', {'news': news})


class NewsDetailsView(DetailView):
    model = Articles
    template_name = 'news/details_view.html'
    context_object_name = 'article'


def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user

            if user.groups.filter(name__in=allowed_roles).exists() or user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You don't have permission to access this page.")

        return _wrapped_view

    return decorator


class GroupRequiredMixin(View):
    @method_decorator(allowed_user(allowed_roles=['admin', 'customer']))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class NewsUpdateView(GroupRequiredMixin, UpdateView):
    model = Articles
    template_name = 'news/create.html'
    form_class = ArticlesForm


class NewsDeleteView(GroupRequiredMixin, DeleteView):
    model = Articles
    success_url = '/news/'
    template_name = 'news/news-delete.html'


@allowed_user(allowed_roles=['admin', 'customer'])
def create(request):
    error = ''
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news_home')
        else:
            error = 'Форма была неверной'

    form = ArticlesForm

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'news/create.html', data)


