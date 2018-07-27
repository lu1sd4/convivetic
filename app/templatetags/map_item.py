from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_list_item(dictionary, key):
    key = key - 1
    if key < dictionary.count():
        return dictionary[key]
    return None