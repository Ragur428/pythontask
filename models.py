
from django.db import models
from django.db.models import Count, Avg
from ckeditor.fields import RichTextField
from django import template
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core.validators import MaxLengthValidator

import random
from account.models import User
import datetime
import os

register = template.Library()

char = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
        'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
        'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


# Create your models here.


def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)


class AddLessons(models.Model):
    lesson_title = models.CharField(max_length=120)
    lesson_description = models.TextField(_('lesson_description'), max_length=500, null=True)
    lesson_video_caption = models.FloatField(_('lesson_video_duration'), null=True)
    video_mode = models.CharField(max_length=15, default="True")
    lesson_video_duration = models.FileField(upload_to=filepath, null=True, blank=True)
    document = models.FileField(upload_to=filepath, null=True, blank=True)
    status = models.CharField(max_length=15, default="True")
    image = models.ImageField(upload_to=filepath, null=True, blank=True)
    audio = models.FileField(upload_to=filepath, null=True, blank=True)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True, null=True, blank=True)


