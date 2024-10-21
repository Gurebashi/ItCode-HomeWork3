import factory
from factory.django import ImageField

from shop import models


class PainterFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    birth_date = factory.Faker('date_of_birth')

    class Meta:
        model = models.Painter


class CategoryFactory(factory.django.DjangoModelFactory):
    category_name = factory.Faker('name')

    class Meta:
        model = models.Category


class StyleFactory(factory.django.DjangoModelFactory):
    style_name = factory.Faker('name')
    style_description = factory.Faker('text')

    class Meta:
        model = models.Style


class PictureFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('sentence')
    cover_picture = ImageField()
    public_date = factory.Faker('date')
    history = factory.Faker('text')
    is_original = factory.Faker('boolean')
    availability = factory.Faker('boolean')
    price = factory.Faker('random_int')
    author = factory.SubFactory(PainterFactory)
    style = factory.RelatedFactory(StyleFactory)
    category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = models.Picture
