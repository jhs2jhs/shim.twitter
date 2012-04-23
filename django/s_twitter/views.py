from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, render_to_response
from django.template import RequestContext
from t_conn.models import Profile, Consumer
from f_conn.models import FConsumer, FOAuth

@login_required
def list_shims(request):
    user = request.user
    twitters = Profile.objects.filter(user=user)
    facebooks = FOAuth.objects.filter(user=user)
    c = RequestContext(request, {'profiles':twitters, 'oauths_facebook':facebooks})
    return render_to_response('list_shim.html', c)
               
