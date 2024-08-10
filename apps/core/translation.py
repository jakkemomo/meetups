from cities_light.loading import get_cities_models
from modeltranslation.translator import TranslationOptions, translator

Country, Region, SubRegion, City = get_cities_models()


class CityTranslationOptions(TranslationOptions):
    fields = ("name", "display_name")


translator.register(City, CityTranslationOptions)
