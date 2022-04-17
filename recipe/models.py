from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class RecipeCategory(models.Model):
    """
    Категории рецептов
    """
    name = models.CharField(_('Category name'),max_length=100)

    class Meta:
        verbose_name = _('Recipe Category')
        verbose_name_plural = _('Recipe Categories')

    def __str__(self):
        return self.name


def get_default_recipe_category():

    return RecipeCategory.objects.get_or_create(name='Other')


class Recipe(models.Model):
    """
    Модель рецептов
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    category = models.ForeignKey(
        RecipeCategory,
        related_name='recipe_list',
        on_delete=models.SET(get_default_recipe_category)
    )
    picture = models.ImageField(upload_to='uploads')
    title = models.CharField(max_length=200)
    desc = models.TextField()
    cook_time = models.TimeField()
    ingredients = models.TextField()
    procedure = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')

    def __str__(self):
        return self.title

    def get_total_number_of_likes(self):
        return self.likes.count()

    def get_total_number_of_bookmarks(self):
        return self.bookmarked_by.count()


class RecipeLike(models.Model):
    """
    лайки рецептов
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username