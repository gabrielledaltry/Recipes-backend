from django.shortcuts import render
from django.http import JsonResponse
from .api_utils import search_recipes_by_name
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Recipe
from .serializers import RecipeSerializer
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt


class RecipeListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)
    
def format_recipe_data(recipe_api_data):
    return {
        'id': recipe_api_data['idMeal'],
        'name': recipe_api_data['strMeal'],
        'image_link': recipe_api_data['strMealThumb'],
        'link': f"https://www.themealdb.com/meal/{recipe_api_data['idMeal']}", # Construct URL
    }

def recipe_search(request):
    """
    Handles GET requests to search for recipes.
    Expects a 'q' query parameter in the URL (e.g., /api/search/?q=chicken)
    """
    if request.method == 'GET':
        query = request.GET.get('q') # Get the search query from URL parameters
        if query:
            results = search_recipes_by_name(query)
            if results:
                # Format each recipe found by the API
                formatted_results = [format_recipe_data(recipe) for recipe in results]
                return JsonResponse({'recipes': formatted_results})
            else:
                # No recipes found for the given query
                return JsonResponse({'recipes': []})
        else:
            # If no search query is provided
            return JsonResponse({'error': 'Please provide a search query.'}, status=400)
    else:
        # Only allow GET requests for this endpoint
        return JsonResponse({'error': 'Only GET requests are allowed.'}, status=405)
    
@csrf_exempt
def check_saved(request, recipe_id):
    if not request.user.is_authenticated:
        return JsonResponse({'saved': False})
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        return JsonResponse({'saved': False})
    saved = recipe.saved_by.filter(id=request.user.id).exists()
    return JsonResponse({'saved': saved})

@csrf_exempt
def save_recipe(request, recipe_id):
    if request.method == 'POST':
        # Implement logic to save the recipe for the user here
        return JsonResponse({'message': f'Recipe {recipe_id} saved!'})
    elif request.method == 'DELETE':
        # Implement logic to unsave the recipe for the user here
        return JsonResponse({'message': f'Recipe {recipe_id} unsaved!'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def save_toggle(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        import json
        data = json.loads(request.body)
        recipe_id = data.get('recipe_id')
        action = data.get('action')
        if not recipe_id or not action:
            return JsonResponse({'error': 'Missing recipe_id or action'}, status=400)
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            return JsonResponse({'error': 'Recipe not found'}, status=404)
        user = request.user
        if action == 'save':
            recipe.saved_by.add(user)
            return JsonResponse({'saved': True, 'message': f'Saved recipe {recipe_id}!'})
        elif action == 'unsave':
            recipe.saved_by.remove(user)
            return JsonResponse({'saved': False, 'message': f'Unsaved recipe {recipe_id}!'})
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

