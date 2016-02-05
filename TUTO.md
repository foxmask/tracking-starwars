## Preambule 

Je sais bien qu'une partie de ce billet ne plaira pas à Sam&Max (thanks to the Django CBV & Mixin:)

## Introduction

La première partie va planter le décors en démarrant par vous montrer comment s'articule une application avec formulaire 
composé d'un sous formulaire en sus (j'expliquerai pourquoi après :) 

Pour ce faire, je vous emmene dans l'univers du 7° art, viendez on va refaire StarWars!

Un modele, un formulaire, une vue, un template et ca sera fini 

## le models.py

```python
    from django.db import models
    
    
    class Movie(models.Model):
        """
            Movie
        """
        name = models.CharField(max_length=200, unique=True)
        description = models.CharField(max_length=200)
    
        def __str__(self):
            return "%s" % self.name
    
    
    class Episode(models.Model):
        """
           Episode - for Trilogy and So on ;)
        """
        name = models.CharField(max_length=200)
        scenario = models.TextField()
        movie = models.ForeignKey(Movie)
    
        def __str__(self):
            return "%s" % self.name
```

## le forms.py, tout rikiki
```python
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

```

## la vue views.py très sèche, enfin DRY ;)

```python
    from django.http import HttpResponseRedirect
    from django.core.urlresolvers import reverse
    from django.views.generic import CreateView, UpdateView, ListView
    
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
```

## Pour finir de planter le décors et les costumes ([merci Roger Hart et Donald Cardwell](https://fr.wikipedia.org/wiki/Au_th%C3%A9%C3%A2tre_ce_soir#Anecdotes))

### base.html
```html
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <title>Manage stories for StarWars</title>
    </head>
    <body>
    <h1>Stories Manager for Starwars</h1>
    {% block content %}
    <a href="{% url 'movie_create' %}">Add a movie</a><br/>
    <h2>Movie list</h2>
    <ul>
    {% for movie in movies %}
    <li><a href="{% url 'movie_edit' movie.id %}">{{ movie.name }}</a></li>
    {% endfor %}
    </ul>
    {% endblock %}
    </body>
    </html>
```

### movie_form.htlm (le template utilisé par les UpdateView & CreateView)

```html
    {% extends "base.html" %}
    {% block content %}
    <form method="post" action="">
        {% csrf_token %}
        {{ formset.management_form }}
        <table>
        {{ form.as_table }}
        </table>
        <table>
        {{ episode_form.as_table }}
        </table>
        <button>Save</button>
    </form>
    {% endblock %}
```

## Mise à jour de la base de données 

cela s'impose :

```bash
(starwars) foxmask@foxmask:~/DjangoVirtualEnv/starwars/starwars $  ./manage.py migrate

Operations to perform:
  Synchronize unmigrated apps: messages, starwars, staticfiles
  Apply all migrations: contenttypes, admin, sessions, auth
Synchronizing apps without migrations:
  Creating tables...
    Creating table starwars_movie
    Creating table starwars_episode
    Running deferred SQL...
  Installing custom SQL...
```

Voilà le tout est prêt, je peux allégrement créer ma double trilogie pépère tel George Lucas.

## Trackons l'impie

Seulement un jour arrive où moi George Lucas, je vends StarWars à Walt Disney, mais comme je veux pas rater 
de ce qu'ils vont faire de mon "bébé", je rajoute un "tracker de modifications" à mon application, 
pour ne pas perdre le "field" de l'Histoire. 

### Installation de Tracking Fields

en prérequis django-tracking-fields requiert django-current-user, donc ze pip qui va bien donne :

```python
    (starwars) foxmask@foxmask:~/DjangoVirtualEnv/starwars/starwars $ pip install django-tracking-fields django-cuser
    Collecting django-tracking-fields
      Downloading django-tracking-fields-1.0.6.tar.gz (58kB)
        100% |████████████████████████████████| 61kB 104kB/s 
    Collecting django-cuser
      Downloading django-cuser-2014.9.28.tar.gz
    Requirement already satisfied (use --upgrade to upgrade): Django>=1.5 in /home/foxmask/DjangoVirtualEnv/starwars/lib/python3.5/site-packages (from django-cuser)
    Installing collected packages: django-tracking-fields, django-cuser
      Running setup.py install for django-tracking-fields ... done
      Running setup.py install for django-cuser ... done
    Successfully installed django-cuser-2014.9.28 django-tracking-fields-1.0.6
```

modification de **settings.py** qui s'impose

```python
    INSTALLED_APPS = (
        ...
        'cuser',
        'tracking_fields',
        ...
    )
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'cuser.middleware.CuserMiddleware',  ## <=== ne pas oublie pour chopper le user qui fait le con avec mes films;)
    )
```

le petit migrate qui va bien aussi pour ajouter les tables pour les modeles de django-tracking-fields

```python
    (starwars) foxmask@foxmask:~/DjangoVirtualEnv/starwars/starwars $  ./manage.py migrate
    Operations to perform:
      Synchronize unmigrated apps: staticfiles, messages, cuser, starwars
      Apply all migrations: auth, sessions, contenttypes, tracking_fields, admin
    Synchronizing apps without migrations:
      Creating tables...
        Running deferred SQL...
      Installing custom SQL...
    Running migrations:
      Rendering model states... DONE
      Applying tracking_fields.0001_initial... OK
      Applying tracking_fields.0002_auto_20160203_1048... OK
```
et nous voilà prêt à joueur les trackers.


### Utilisation

On ne peut pas rêver plus simple, cela se résume à un décorateur sur le modele qui identifie quelles données sont modifiées, 
et un field ̀`histo` qui va lier le modele TrackingEvent de l'application TrackingFields, à ma table à surveiller. 
Et là, bien que le modele ait été modifié, inutile de faire un nouveau "python manage.py migrate", rien ne bougera, 
car histo sera une [GenericRelation()](https://docs.djangoproject.com/fr/1.8/ref/contrib/contenttypes/#generic-relations).
En effet, TrackingEvent repose sur [ContenType](https://docs.djangoproject.com/fr/1.9/ref/contrib/contenttypes/) aka "L'Infrastructure des Types de Contenu". Si vous avez déjà tripoté la gestion des permissions, vous avez déjà dû vous y frotter;)


Pour la faire courte, en clair ça donne :


#### models.py

```python
    from django.db import models
    from django.contrib.contenttypes.fields import GenericRelation
    
    from tracking_fields.decorators import track
    from tracking_fields.models import TrackingEvent
    
    
    @track('name', 'description')
    class Movie(models.Model):
        """
            Movie
        """
        name = models.CharField(max_length=200, unique=True)
        description = models.CharField(max_length=200)
        histo = GenericRelation(TrackingEvent, content_type_field='object_content_type')
    
        def episodes(self):
            return Episode.objects.filter(movie=self)
    
        def __str__(self):
            return "%s" % self.name
    
    @track('name', 'scenario')
    class Episode(models.Model):
        """
           Episode - for Trilogy and So on ;)
        """
        name = models.CharField(max_length=200)
        scenario = models.TextField()
        movie = models.ForeignKey(Movie)
        histo = GenericRelation(TrackingEvent, content_type_field='object_content_type')
    
        def __str__(self):
            return "%s" % self.name
```

bon là c'est simplissime comme une recette de pate à crêpes: 3 imports de rigueur, le décorateur et la GenericRelation() on mélange le tout et ca donne ce qui suit 
J'ai, au passage, rajouté une fonction `episodes` à ma classe Movie, dont je vous reparlerai plus bas.

### le template de la DetailView qui va bien

```html
    <table>
       <caption>History of the modification of {{ object }} </caption>
       <thead>
       <tr><th>Old Value</th><th>New Value</th><th>By</th><th>at</th></tr>
       </thead>
       <tbody>
    {% for h in object.histo.all %}
       {% for f in h.fields.all %}
           <tr><td>{{ f.old_value }}</td><td>{{ f.new_value }}</td><td>{{ h.user }}</td><td>{{ h.date }}</td></tr>
       {% endfor %}
    {% endfor %}
       </tbody>
    </table>
```
A présent si je me rends dans ma page pour modifier le scénario d'un Episode, mon template ci dessus, ne m'affichera pas ces modications !
Pourquoi bou diou ? Parce qu'ici j'affiche "l'histo" de Movie pas de Episode... On comprend à présent ici mon intéret pour 
le sous formulaire. Le "problème" aurait été masqué si je m'étais arrêté à un seul simple formulaire. 


### Corrigeons 

c'est là qu'entre en jeu la fonction `episodes` à ma classe Movie, pour me permettre d'itérer dessus et afficher tout le toutim 

#### le template de la DetailView qui va bien (bis)

```html
    <table>
        <caption>History of the modifications of {{ object }} </caption>
        <thead>
            <tr><th>Old Value</th><th>New Value</th><th>By</th><th>at</th></tr>
        </thead>
        <tbody>
    {% for h in object.histo.all %}
       {% for f in h.fields.all %}
           <tr><td>{{ f.old_value }}</td><td>{{ f.new_value }}</td><td>{{ h.user }}</td><td>{{ h.date }}</td></tr>
       {% endfor %}
    {% endfor %}
        </tbody>
    </table>
    {% for ep in object.episodes %}
        {% if ep.histo.all %}
    <table>
        <caption>history of the modifications of Episode</caption>
        <thead>
            <tr><th>Old Value</th><th>New Value</th><th>By</th><th>at</th></tr>
        </thead>
        <tbody>
            {% for h in ep.histo.all %}
                {% for f in h.fields.all %}
                {% if f.old_value == f.new_value %} {# they are the same when the new value is created to avoid to display "null" #}
                {% else %}
                <tr><td>{{ f.old_value }}</td><td>{{ f.new_value }}</td><td>{{ h.user }}</td><td>{{ h.date }}</td></tr>
                {% endif %}
                {%  endfor %}
            {% endfor %}
        </tbody>
     </table>
        {% endif %}
    {% endfor %}
```

Voili voilou ! Et en prime, si vous êtes curieux, coté admin, vous avez aussi la liste de toutes les modifications si besoin ;)

Aux utilisateurs avertis qui diraient :

> pourquoi l'avoir recodé coté front puisque c'est déjà géré coté admin sans lever le petit doigt ?

Parce que George Lucas veut montrer les modifications apportées à son bébé StarWars par Walt Disney, au monde entier pardis ! 

Ah un détail en passant : dans l'admin la vue qui affiche la liste des modifications donne : "Episode Object" ou "Movie Object". 
Pour eviter ça, zavez dû remarqué que j'ai mis la fonction **__str__** dans mes modèles ce qui vous rendra une valeur 
plus "lisible" sur ce qui a été modifié.


## Conclusion : 

Dans la vraie vie de votre serviteur, je ne me voyais pas créer un modele "history" lié "physiquement" par une FK
à chaque modèle, j'entreprenais de chercher au travers de la toile quelques ressources.

C'est finallement sur [#django-fr@freenode](irc://irc.freenode.net/django-fr) que j'ai posé la question et ai obtenu
de [Gagaro](https://github.com/gagaro) le grââl : une application nommée [tracking-fields](https://github.com/makinacorpus/django-tracking-fields), dont il est l'auteur.

Pour une fois que je fais ma faignasse en ne codant pas tout by myself, [ça fait plaisir de tomber sur une appli pareille](https://github.com/makinacorpus/django-tracking-fields) ! 


Si vous voulez jouer avec le code de ce gestionnaire de films [c'est par ici la bonne soupe](https://github.com/foxmask/tracking-starwars)
