from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from .forms import SignUpForm, ConnectionForm
from .models import ProductsA, UserProducts
from .callapi import Callapi
import json




def home_page(request):
    """
        Return the home page of the application
    """
    return render(request, 'substitution_app/home_page.html')


def signup(request):
    """
        Generate the display of the registration form page.
    """
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(home_page)
    else:
        form = SignUpForm()
    return render(request, 'substitution_app/signup.html', {'form': form})


def connection(request):
    """
        Generate the display of the login form page.
    """
    error = False
    if request.method == "POST":
        form = ConnectionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            # Check if the data is correct
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return render(request, 'substitution_app/home_page.html',
                              locals())
            else:
                error = True
    else:
        form = ConnectionForm()

    return render(request, 'substitution_app/connection.html', locals())


def deconnection(request):
    """
        Management of user disconnection.
    """
    logout(request)
    return redirect(reverse(home_page))


def myaccount(request):
    """
        Management of the user's account page.
    """
    username = None
    if request.user.is_authenticated:
        context = {
            "username" : request.user.username,
            "usermail" : request.user.email
        }
        return render(request, 'substitution_app/myaccount.html', context)


def product_select(request):
    """
        Management of the search and display of the result of the request of the user
    """
    callapi = Callapi()
    if request.method == 'POST':
        try:
            userQuery = request.POST.get('userQuery')
            apiQuery = callapi.request_the_openfoodfact_api(userQuery)

        except:
            raise Http404("Erreur 404")
        else:
            apiQuery = callapi.clean_the_openfoodfact_api_request(apiQuery)  
            if apiQuery:

                return render(request, 'substitution_app/product_select.html',
                            {'apiQuery': apiQuery, 'userQuery' : userQuery})
            else:
                return render(request, 'substitution_app/noProdFound.html',
                            {'userQuery' : userQuery})


def results(request, code):
    """
        Management of the search and display of the result
        of the query for substitute products.
    """
    callapi = Callapi()
    apiQuery = callapi.barcode_request_the_openfoodfact_api(code)
    apiQuery = callapi.barcode_clean_the_oppenfoodfact_api_request(apiQuery)

    if apiQuery == 404:
        raise Http404("Erreur 404")
    else:
        # Search first for a substitute in the database
        categorie = apiQuery['categories_hierarchy'][0]
        substitution = ProductsA.objects.filter(main_category__contains=categorie)
        if substitution.exists():
            return render(request, 'substitution_app/results.html',
                          {'apiQuery': apiQuery, 'substitution': substitution})
        else:
            # Otherwise, search for a substitute in the OFF API
            substitution = callapi.request_for_substitution_products_in_openfoodfact_api(apiQuery)
            substitution = callapi.clean_substitution_products_in_openfoodfact_api(substitution)
            if substitution is None:
                return render(request, 'substitution_app/noSubProdFound.html',
                          {'apiQuery': apiQuery})

            return render(request, 'substitution_app/results.html',
                          {'apiQuery': apiQuery, 'substitution': substitution})


def my_products(request):
    """
    Manages the registration of the substituted products in the database
    as well as their display on the user's page.
    """
    # Search for substituted products by user.
    username = request.user.username
    user_products = UserProducts.objects.filter(username=username)
    context = {
        'user_products' : user_products
    }
    # If the request is POST, the product is saved in the database.
    if request.method == 'POST':
        if request.user.is_authenticated:
            products_save = UserProducts.objects.create(
                username=request.user.username,
                code=request.POST.get('code'),
                url=request.POST.get('url'),
                product_name=request.POST.get('product_name'),
                nutrition_grade_fr=request.POST.get('nutrition_grade_fr'),
                main_category=request.POST.get('main_category'),
                main_category_fr=request.POST.get('main_category_fr'),
                image_small_url=request.POST.get('image_small_url')
            )
            return render(request, 'substitution_app/myproducts.html', context)
    else:
        if request.user.is_authenticated:
            return render(request, 'substitution_app/myproducts.html', context)
        else:
            return redirect(connection)


def product_display(request, code):
    """
        Manages the display of the detail of a product.
    """
    callapi = Callapi()
    apiQuery = callapi.barcode_request_the_openfoodfact_api(code)
    if apiQuery == 404:
        raise Http404("Erreur 404")
    else:
        apiQuery = callapi.barcode_clean_the_oppenfoodfact_api_request(apiQuery)

        return render(request, 'substitution_app/product_display.html', {'apiQuery': apiQuery})

def LegalNotice(request):
    return render(request,'substitution_app/legal.html')
