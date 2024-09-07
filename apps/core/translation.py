from modeltranslation.translator import TranslationOptions, translator

from apps.core.models import City


class CityTranslationOptions(TranslationOptions):
    fields = ("name", "display_name")


translator.register(City, CityTranslationOptions)
