import factory
from django.utils.timezone import now

from recipe.models import Recipe, RecipeLike, RecipeCategory
from users.tests.factories import UserFactory


class RecipeCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RecipeCategory

    name = factory.Faker('word')


class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recipe

    author = factory.SubFactory(UserFactory)
    category = factory.SubFactory(RecipeCategoryFactory)
    picture = factory.Faker('image_url')
    title = factory.Faker('sentence')
    desc = factory.Faker('sentence')
    cook_time = factory.LazyAttribute(lambda x: now())
    ingredients = factory.Faker('text')
    procedure = factory.Faker('text')


class RecipeLikeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RecipeLike

    user = factory.SubFactory(UserFactory)
    recipe = factory.SubFactory(RecipeFactory)

