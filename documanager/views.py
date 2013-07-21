from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotAllowed
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from documanager.forms import MarkdownForm
from documanager.models import Stationary
from documanager.utils import make_html
from django.template.loader import render_to_string
from wsgiref.util import FileWrapper
from pywkher import generate_pdf
import pystmark
import json

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
                return HttpResponse(FileWrapper(pdf_file),
                        content_type = 'application/pdf')
    else:
        form = MarkdownForm()
    
    if not Stationary.objects.all():
        context_dict['no_stationary'] = "There are no stationaries"

    context_dict['form'] = form
    return render_to_response("documanager/home.html",
                               context_dict, 
                               context_instance=RequestContext(request)
                              )    

def process_inbound(request):
    pass

def email_pdf(request):
    if request.method == 'POST':    
        try:
            data = json.loads(request.body)
        except ValueError:
            return HttpResponseBadRequest("No JSON provided")
        try: 
            msubject = data['Subject']
            mfrom = data['From']
            mbody = data['TextBody']
        except KeyError:
                return HttpResponseBadRequest("Invalid JSON")
    
        # Now let's create the pdf
        try:
            styling = Stationary.objects.get(name__icontains='msubject').styling
        except ObjectDoesNotExist: 
            styling = '' 

        rendered_html = render_to_string('documanager/print_render.html',
                                        {'html':mbody, 'styling':styling})

        pdf_file = generate_pdf(html=rendered_html)
        PM_API_KEY = getattr(settings, "PM_API_KEY", None)
        PM_SENDER =  getattr(settings, "PM_SENDER", None)

        message = pystmark.Message(sender=PM_SENDER, to=mfrom, 
                                   subject = 'Hi', text = 'Your email should (not yet) be attached',
                                   tag = 'greeting')
        pystmark.send(message, api_key=PM_API_KEY)


        return HttpResponse("Success!")


    else:
        return HttpResponseNotAllowed(['POST'])

def sent_confirm(request):
    return HttpResponse("Your email has been sent")
