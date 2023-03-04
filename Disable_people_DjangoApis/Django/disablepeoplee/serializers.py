from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from .models import *
from django_jalali.serializers.serializerfield import JDateField, JDateTimeField
from django.contrib.auth.models import User
class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12] 
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension
        
    
class CameraSerializer(serializers.ModelSerializer):
        
    class Meta:
        model= CameraInfo
        fields = '__all__'
        
class userSerializer(serializers.ModelSerializer):
        
    class Meta:
        model= User
        fields= ['username','password']
              
        
class DetectSeializer(serializers.ModelSerializer):
 
    img = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model=Detects
        fields= ['classobj','boundry','date_created','img','lightflag','date2']
        
        
        
        
class DetectSeializer1(serializers.ModelSerializer):      
    date2 = JDateField()
    img = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model=Detects
        fields= ['classobj','boundry','date_created','img','lightflag','date2']
        exclude = []
        