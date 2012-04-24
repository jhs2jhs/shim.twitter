from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, render_to_response
from django.template import RequestContext
from t_conn.models import Profile, Consumer
from f_conn.models import FConsumer, FOAuth
from catalog.models import CResource, CRAccess

@login_required
def list_shims(request):
    print request.get_host()
    user = request.user
    rs = []
    resources = CResource.objects.filter(user=user)
    for resource in resources:
        r_a = ''
        accesss = CRAccess.objects.filter(resource=resource)
        #print accesss
        #for access in accesss:
        #    r_a += '<a href=\'%s\'>%s</a> '%(access.token, access.token)
        r = {'r':resource, 'r_a':accesss}
        print r
        rs.append(r)
    twitters = Profile.objects.filter(user=user)
    facebooks = FOAuth.objects.filter(user=user)
    c = RequestContext(request, {'profiles':twitters, 'oauths_facebook':facebooks, 'resources':rs})
    return render_to_response('list_shim.html', c)
               
