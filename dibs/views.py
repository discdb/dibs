from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from secrets import token_urlsafe

from .models import ImageModel
from .serializers import ImageSerializer

@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload(request):
    #todo: check for dupes
    try:
        imgsize = len(request.data['image'].read())
        newimg = ImageModel(imgfile=request.data['image'], userid=request.data['userid'], imageid=token_urlsafe(settings.UID_LENGTH_BYTES), filesize=imgsize)
        newimg.save()
    except TypeError:
        return Response('Image format not supported.', status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    ser = ImageSerializer(newimg)
    return Response(ser.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def info(request, image_id):
    try:
        img = ImageModel.objects.get(imageid=image_id)
        ser = ImageSerializer(img)
        return Response(ser.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        #no image with that ID found
        return Response('No image with that ID exists.', status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'DELETE'])
def image(request, image_id):
    if request.method == 'GET':
        try:
            img = ImageModel.objects.get(imageid=image_id)
            #return the image
            #this needs to be an HttpResponse instead of a REST response because an image isn't UTF-8 encoded, it's raw bytes
            #magically, 'image/png' also works with jpegs.
            return HttpResponse(img.imgfile, content_type='image/png', status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            #no image with that ID found
            return Response('No image with that ID exists.', status=status.HTTP_204_NO_CONTENT)
    else: #DELETE
        num_deleted = ImageModel.objects.filter(imageid=image_id).delete()[0]
        if num_deleted > 0:  #this should NEVER be > 1
            return Response('Image deleted.', status=status.HTTP_200_OK)
        else:
            #no image with that ID found
            return Response('No image with that ID exists.', status=status.HTTP_204_NO_CONTENT)