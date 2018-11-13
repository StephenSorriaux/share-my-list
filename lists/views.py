from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import List, Choice, Person
from django.contrib.auth import logout
from .utils import isfloat

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('lists:index'))


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'lists/index.html'
    context_object_name = 'all_lists'

    def get_queryset(self):
        return List.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['current_user'] = self.request.user.username
        return context

class DetailView(generic.DetailView):
    model = List
    template_name = 'lists/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['current_user'] = self.request.user.username
        return context

def create(request):
    person = get_object_or_404(Person, pk=request.user.id)
    obj, created = List.objects.get_or_create(
        owner=person
    )
    if obj is not None:
        messages.add_message(request, messages.INFO, "Vous avez déjà une liste, petit rigolo !")
    return HttpResponseRedirect(reverse('lists:index'))


def add(request, list_id):
    list = get_object_or_404(List, pk=list_id)
    if request.POST['name'] is not None and isfloat(request.POST['price']):
        choice = Choice.objects.create(
            list=list,
            article_text=request.POST['name'],
            link_text=request.POST['link'],
            price=request.POST['price']
        )
        return HttpResponseRedirect(reverse('lists:detail', args=(list.id,)))
    else:
        messages.add_message(request, messages.WARNING, "Le nom du cadeau n'a pas été défini ou le prix n'est pas un chiffre")
        return HttpResponseRedirect(reverse('lists:detail', args=(list.id,)))


def make_available(request, list_id, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    choice.is_bought = False
    choice.is_bought_by = None
    choice.save()
    return HttpResponseRedirect(reverse('lists:detail', args=(list_id,)))

def update(request, list_id):
    list = get_object_or_404(List, pk=list_id)
    person = get_object_or_404(Person, pk=request.user.id)

    if list.owner.id == request.user.id:
        messages.add_message(request, messages.WARNING, "Vous ne pouvez pas marquer un cadeau comme pris.")
        return HttpResponseRedirect(reverse('lists:detail', args=(list.id,)))
    
    try:
        selected_choice = list.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'lists/detail.html', {
            'list': list,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.is_bought = True
        selected_choice.is_bought_by = person
        selected_choice.save()
        return HttpResponseRedirect(reverse('lists:detail', args=(list.id,)))