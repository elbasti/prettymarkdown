from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from documanager.forms import MarkdownForm
from documanager.models import Stationary
from documanager.utils import make_html
from django.template.loader import render_to_string
from wsgiref.util import FileWrapper
from pywkher import generate_pdf
# Create your views here.

def index(request):
    context_dict = {}
    
    if request.method == 'POST':
        form = MarkdownForm(request.POST)
        if form.is_valid():
            html = make_html(form.cleaned_data['markdown_input']) 
            context_dict['html'] = html
            styling = form.cleaned_data['stationary'].styling
            render_dict =  {'html':html, 'styling':styling}

            if 'generate' in request.POST:
                return render_to_response('documanager/browser_render.html',
                    render_dict,
                    context_instance = RequestContext(request))

            elif 'print' in request.POST:
                rendered_html = render_to_string('documanager/print_render.html',
                                render_dict)
            
                pdf_file = generate_pdf(html=rendered_html)
                response = HttpResponse(FileWrapper(pdf_file),
                        content_type = 'application/pdf')
                return response
    else:
        form = MarkdownForm()
    
    if not Stationary.objects.all():
        context_dict['no_stationary'] = "There are no stationaries"

    context_dict['form'] = form
    return render_to_response("documanager/home.html",
                               context_dict, 
                               context_instance=RequestContext(request)
                              )    
