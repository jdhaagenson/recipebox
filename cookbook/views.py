from django.shortcuts import render
from cookbook.models import Recipe
from cookbook.models import Author
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import get_object_or_404, reverse, HttpResponseRedirect
from django.http import HttpResponseForbidden
from cookbook.forms import AddRecipeForm, AddAuthorForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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
    favorite_recipe = request.user.author.favorites.all()
    return render(request, 'author_details.html',
                  {'author': author, 'recipes': recipes, 'favorites': favorite_recipe})
    
@login_required
def favorites_view(request, favorites_id):
    current_user = request.user
    favorite = Recipe.objects.filter(id=favorites_id).first()
    current_user.author.favorites.add(favorite)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
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
            return HttpResponseRedirect(request.GET.get('next', reverse("homepage")))
    form = AddRecipeForm()
    return render(request, 'add_recipe.html', {'form': form})


@login_required
def edit_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    if request.user.author.id == recipe.author.id or request.user.is_staff:
        
        if request.method == "POST":
            form = AddRecipeForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                recipe.title = data["title"]
                recipe.instructions = data["instructions"]
                recipe.time_required = data["time_required"]
                recipe.description = data["description"]
                recipe.save()
            return render(reverse("add_recipe", args=[recipe.id]))
    
    
        data = {
            "title": recipe.title,
            "instructions": recipe.instructions,
            "time_required": recipe.time_required,
            "description": recipe.description
        }
        form = AddRecipeForm(initial=data)
        return render(request, "add_recipe.html", {"form": form})
    
    return HttpResponseForbidden("You don't have permission to do this")


@login_required
def author_form_view(request):
    if request.method == 'POST':
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data.get('username'),
                password=data.get('password'))
            author = Author.objects.create(
                name=data.get('name'),
                bio=data.get('bio'),
                user = user
            )
            author.save()
            if request.user.is_staff:
                return HttpResponseRedirect(request.GET.get('next', reverse("homepage")))
    form = AddAuthorForm()
    return render(request, 'add_author.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get('username'), password=data.get("password"))
            if user:
                login(request, user)
    #            return HttpResponseRedirect(reverse("homepage"))
                return HttpResponseRedirect(request.GET.get(next, reverse("homepage")))
    form = LoginForm()
    return render(request, "loginpage.html", {"form": form})


# @login_required()
# def author_form_view(request):
#     html = "generic_form.html"
#     form = AddAuthorForm()
#     if request.method == "POST":
#         form = AddAuthorForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             user = User.objects.create_user(
#                 username=data.get('name')
#             )
#             author = Author.objects.create(
#                 name=data.get('name'), bio=data.get('bio'), user=user)
#             author.save()
#         return HttpResponseRedirect(
#             request.GET.get('next', reverse('homepage')))
#     if request.user.is_staff:
#         return render(request, html, {"form": form})
#     return render(request, '')
# def signup_form_view(request):
#     if request.method == "POST":
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             data = form.cleaned_data
#             new_user = User.objects.create_user(
#                 username=data.get('username'),
#                 password=data.get('password')
#             )
#             new_user = authenticate(request, data.get('username', data.get('password')))
#             login(request, new_user)
#             return HttpResponseRedirect(request.GET.get(next, reverse("homepage")))
#
#     form = SignupForm()
#     return render(request, "signup.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))


def error_view(request):
    return HttpResponseRedirect(reverse("error"))