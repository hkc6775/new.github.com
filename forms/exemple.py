from django.utils.encoding import force_str
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


def get_url(request):
    print(get_current_site(request))
    print(urlsafe_base64_encode(force_str('clauvis')))
    
get_url()