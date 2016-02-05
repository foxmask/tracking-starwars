from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView

from starwars.models import Movie
from starwars.forms import MovieForm, EpisodeFormSet


class MovieMixin(object):
    model = Movie
    form_class = MovieForm

    def get_context_data(self, **kw):
        context = super(MovieMixin, self).get_context_data(**kw)
        if self.request.POST:
            context['episode_form'] = EpisodeFormSet(self.request.POST)
        else:
            context['episode_form'] = EpisodeFormSet(instance=self.object)
        return context

    def get_success_url(self):
        return reverse("home")

    def form_valid(self, form):
        formset = EpisodeFormSet((self.request.POST or None), instance=self.object)
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()

        return HttpResponseRedirect(reverse('home'))


class Movies(ListView):
    model = Movie
    context_object_name = "movies"
    template_name = "base.html"


class MovieCreate(MovieMixin, CreateView):
    """
        MovieMixin manage everything for me ...
    """
    pass


class MovieUpdate(MovieMixin, UpdateView):
    """
        ... and I'm DRY :D
    """
    pass


class MovieDetail(DetailView):
    model = Movie

