from django.conf import settings
from django.urls import path, re_path

from .views import image, info, upload

urlpatterns = [
    path('', upload, name='upload'),
    #match a string of length UID_LENGTH while chars from the base64url charset (A-Z,a-z,0-9,_,-)
    re_path(r'^(?P<image_id>[a-zA-Z0-9_-]{' + str(settings.UID_LENGTH) + r'})/$', image, name='image'),
    #see above, but add "/information/" onto the end
    re_path(r'^(?P<image_id>[a-zA-Z0-9_-]{' + str(settings.UID_LENGTH) + r'})/information/$', info, name='info')
]