from django.db import models
import os
from django.conf import settings
from django.utils.html import mark_safe
import datetime
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _
import binascii

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def Profile_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.pk}-{name}{ext}"
    x = f"Image/{final_name}"
    return x



class CameraInfo(models.Model):
    
    cameraip=models.IntegerField()
    date_created = models.DateField(verbose_name="تاریخ تشخیص")

    
   
    def __repr__(self):
        return f'{self.id}-{self.cameraname}-{self.date_created}' 

        
        
    class Meta:
        verbose_name = (" دوربین")
        verbose_name_plural = ("دوربین ها")
    
def mainproductFile(instance, filename):
    dateti = str(datetime.datetime.now().year)+"_" + \
        str(datetime.datetime.now().month)+"_"+str(datetime.datetime.now().day)
    return '/'.join([dateti,str(instance.date_created)+".jpg"])


class Detects(models.Model):
    
    classobj=models.IntegerField()
    boundry=models.CharField(max_length=60, verbose_name='مختصات ')
    date_created=models.DateField(verbose_name="تاریخ تشخیص",auto_now_add=True) 
    date2=jmodels.jDateField()
    img = models.ImageField(
         verbose_name="فریم",upload_to=mainproductFile)
    cameraid= models.ForeignKey(CameraInfo, on_delete=models.CASCADE,default=1)
    lightflag=models.BooleanField(verbose_name="چراغ",default=False,null=True,blank=True)

    def __str__(self):
            return str(self.date_created)
        
        
    class Meta:
        verbose_name = ("اشیا تشخیص داده شده")
        verbose_name_plural = ("اشیا تشخیص داده شده")




class MyToken(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)

   
    user = models.OneToOneField(
        User, related_name='user_token',
        on_delete=models.CASCADE, )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(MyToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key




@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        


