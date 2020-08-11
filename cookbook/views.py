from django.shortcuts import render
from cookbook.models import Recipe
from cookbook.models import Author
from django.shortcuts import get_object_or_404, reverse, HttpResponseRedirect
from cookbook.forms import AddRecipeForm, AddAuthorForm

# Create your views here.


def main(request):
    recipes = Recipe.objects.all()
    return render(request, 'main.html', {'recipes': recipes,
                                         'addauthor': author_form_view,
                                         'addrecipe': recipe_form_view})


def recipe_details(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, template_name="recipe_details.html",
                  context={'recipe': recipe})


def author_details(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    recipes = Recipe.objects.filter(author=author_id)
    return render(request, 'author_details.html',
                  {'author': author, 'recipes': recipes})


def recipe_form_view(request):
    if request.method == 'POST':
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data.get('title'),
                author=data.get('author'),
                instructions=data.get('instructions'),
                time_required=data.get('time_required'),
                description=data.get('description')
            )
            return HttpResponseRedirect(reverse("homepage"))
    form = AddRecipeForm()
    return render(request, 'add_recipe.html', {'form': form})


def author_form_view(request):
    if request.method == 'POST':
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Author.objects.create(
                name=data.get('name'),
                bio=data.get('bio')
            )
            return HttpResponseRedirect(reverse("homepage"))
    form = AddAuthorForm()
    return render(request, 'add_author.html', {'form': form})
