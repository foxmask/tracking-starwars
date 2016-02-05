from django import forms
from django.forms.models import inlineformset_factory

from starwars.models import Movie, Episode


class MovieForm(forms.ModelForm):

    class Meta:
        """
            As I have to use : "exclude" or "fields"
            As I'm very lazy, I dont want to fill the list in the "fields"
            so I say that I just want to exclude ... nothing :P
        """
        model = Movie
        exclude = []

# a formeset based on the model of the Mother "Movie" and Child "Episode" + 1 new empty lines
EpisodeFormSet = inlineformset_factory(Movie, Episode, fields=('name', 'scenario'), extra=1)

