from django.contrib import admin

from .models import Recipe, RecipeLike, RecipeCategory

admin.site.register(RecipeCategory)
admin.site.register(Recipe)
admin.site.register(RecipeLike)
