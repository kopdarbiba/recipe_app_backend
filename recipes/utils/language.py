
def get_localized_field(obj, lang_param):
    if lang_param:
        localized_value = getattr(obj, lang_param)
        if localized_value is not None:
            return localized_value
    # Return a default value or handle the case where lang_param is not found
    return ""

class LanguageMixin:
    def get_localized_field(self, obj):
        lang_param = self.context['request'].GET.get('language')
        return get_localized_field(obj, lang_param)
