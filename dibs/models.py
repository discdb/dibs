from datetime import datetime
from django.conf import settings
from django.db.models import CharField, ImageField, Model
from os.path import join


class ImageModel(Model):
    # this function is black magic, only touch it if you know more than I do
    def upload_rename(path):
        def wrapper(instance, filename):
            ext = filename.split('.')[-1]
            filename = str(instance.imageid) + '.' + ext
            return join(path, filename)
        return wrapper
        
    imageid = CharField(max_length=settings.UID_LENGTH, default='', unique=True)  #this is NOT the primary key
    imgfile = ImageField(upload_to=upload_rename(settings.IMAGE_FOLDER))
    #YYYY-MM-DD HH:MM isn't technically ISO 8601 compliant, but it's short and human readable.
    datestamp = CharField(max_length=16, default=datetime.utcnow().strftime("%Y-%m-%d %H:%M"))
    filesize = CharField(max_length=30, default='0')
    userid = CharField(max_length=30, default='')
