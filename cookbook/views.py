from django.shortcuts import render
from cookbook.models import Recipe
from cookbook.models import Author
from django.shortcuts import get_object_or_404

# Create your views here.


def main(request):
    recipes = Recipe.objects.all()
    return render(request, 'main.html', {'recipes': recipes})


def recipe_details(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, template_name="recipe_details.html",
                  context={'recipe': recipe})


def author_details(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    recipes = Recipe.objects.filter(author=author_id)
    return render(request, 'author_details.html',
                  {'author': author, 'recipes': recipes})
