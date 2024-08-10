from modeltranslation.translator import translator, TranslationOptions
from cities_light.loading import get_cities_models

Country, Region, SubRegion, City = get_cities_models()


class CityTranslationOptions(TranslationOptions):
    fields = ('name', 'display_name')


translator.register(City, CityTranslationOptions)
