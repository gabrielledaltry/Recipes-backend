from django.contrib import admin
from django.urls import path
from .views import RecipeListView

urlpatterns = [
    path('recipes/', RecipeListView.as_view(), name='recipe-list'),
]