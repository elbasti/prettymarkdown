from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from documanager.forms import MarkdownForm
# Create your views here.

def index(request):
    form = MarkdownForm()
    return render_to_response("documanager/home.html",
                               {'form':form}, 
                               context_instance=RequestContext(request)
                              )

