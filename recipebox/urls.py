"""recipebox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cookbook.views import recipe_form_view, \
    recipe_details, author_details, main, author_form_view, \
    login_view, logout_view, error_view, edit_recipe, favorites_view

urlpatterns = [
    path('', main, name="homepage"),
    path('loginpage/', login_view, name="login_view"),
    path('logout/', logout_view, name="logout_view"),
    path('addrecipe/', recipe_form_view, name="add_recipe"),
    path('addauthor/', author_form_view, name="add_author"),
    path('author/<int:author_id>', author_details, name="author_details"),
    path('recipe/<int:recipe_id>', recipe_details, name="recipe_details"),
    path('recipe/<int:recipe_id>/edit/', edit_recipe, name="edit_recipe" ),
    path('favorites/<int:favorites_id>/', favorites_view, name="favorites"),
    path('admin/', admin.site.urls),
    path('error/', error_view, name="error"),
]
