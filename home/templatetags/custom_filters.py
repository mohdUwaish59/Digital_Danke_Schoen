from django import template
import os

register = template.Library()

@register.filter(name='splitext')
def splitext(value):
    root, ext = os.path.splitext(value)
    return (root, ext)

ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']

@register.filter
def is_image(filename):
    return any(filename.lower().endswith(extension) for extension in ALLOWED_IMAGE_EXTENSIONS)