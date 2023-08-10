from django import template
import json

register = template.Library()

@register.filter
def jsonify(obj):
    return json.dumps(obj)

# Rest of the code...
