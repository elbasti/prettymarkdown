from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from documanager.forms import MarkdownForm
from documanager.models import Stationary
from documanager.utils import make_html
# Create your views here.

def index(request):
    context_dict = {}
    
    if request.method == 'POST':
        form = MarkdownForm(request.POST)
        if form.is_valid():
            html = make_html(form.cleaned_data['markdown_input']) 
            context_dict['html'] = html
            if 'generate' in request.POST:
                styling = form.cleaned_data['stationary'].styling
                return render_to_response('documanager/browser_render.html',
                    {'html':html, 'styling':styling},
                    context_instance = RequestContext(request))
    else:
        form = MarkdownForm()
    
    if not Stationary.objects.all():
        context_dict['no_stationary'] = "There are no stationaries"

    context_dict['form'] = form
    return render_to_response("documanager/home.html",
                               context_dict, 
                               context_instance=RequestContext(request)
                              )

def print_to_browser(request):
    if request.method == 'POST':
        return HttpResponse("woot woot")
    else: 
        return HttpResponseRedirect(reverse('documanager:index'))
