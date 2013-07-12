from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from documanager.forms import MarkdownForm
from documanager.models import Stationary
# Create your views here.

def index(request):
    context_dict = {}
    
    form = MarkdownForm()
    stationaries = Stationary.objects.all()
    if not stationaries:
        context_dict['no_stationary'] = "There are no stationaries"

    context_dict['form'] = form
    return render_to_response("documanager/home.html",
                               context_dict, 
                               context_instance=RequestContext(request)
                              )

