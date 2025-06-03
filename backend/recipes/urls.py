from django.contrib import admin
from django.urls import path
from . import views
from .views import RecipeListView, recipe_search, check_saved, save_toggle

urlpatterns = [
    path('recipes/', RecipeListView.as_view(), name='recipe-list'),
    path('search/', recipe_search, name='recipe_search'),
    path('check_saved/<int:recipe_id>/', check_saved, name='check_saved'),
    path('save_toggle/', save_toggle, name='save_toggle'),
]