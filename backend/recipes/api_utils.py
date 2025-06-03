# backend/recipes/api_utils.py
import requests

BASE_URL = "https://www.themealdb.com/api/json/v1/1/"

def search_recipes_by_name(query):
    """Searches for recipes by name using The Meal DB API."""
    endpoint = f"{BASE_URL}search.php"
    params = {"s": query}
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('meals')  # Returns a list of meal objects or None
    except requests.exceptions.RequestException as e:
        print(f"Error searching recipes on MealDB: {e}")
        return None
