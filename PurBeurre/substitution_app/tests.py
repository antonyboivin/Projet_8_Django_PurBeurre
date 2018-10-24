from django.contrib import auth
from django.urls import reverse
from django.test import TestCase
from .models import ProductsA, UserProducts
from .callapi import Callapi




class Userjourney(TestCase):

    def test_home_page(self):
        """
        As Lily I have to be able to access the site by entering the URL in my browser.
        En tant que Lily je dois pouvoir accéder au site en rentrant l'URL dans mon navigateur.
        """
        response = self.client.get(reverse('home page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'substitution_app/home_page.html')

    def test_search_for_product(self):
        """
        As Lily, I must be able to enter a product to substitute in a search field and validate.
        En tant que Lily, je dois pouvoir entrer un produit à substituer dans un champ de recherche et valider.
        """
        userQuery = 'nutella'
        apiQuery = [{'product_name_fr': 'Nutella', 
                    'code': '3017620429484', 
                    'nutrition_grade_fr': 'e', 
                    'categories_hierarchy': ['fr:pates-a-tartiner'], 
                    'categories': 'Desayunos,Untables,Untables dulces,Cremas para untar,Cremas de chocolate,Cremas a base de avellanas,Cremas de cacao y avellanas,Pâtes à tartiner', 
                    'image_small_url': 'https://static.openfoodfacts.org/images/products/301/762/042/9484/front_fr.147.200.jpg'}]


        response = self.client.post(reverse('product select'), {'apiQuery': apiQuery, 'userQuery' : userQuery})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'substitution_app/product_select.html')

    
    def test_display_products_research(self):
        """
        As Lily, I'm waiting for the app to show me all the products matching my search.
        En tant que Lily, j'attends que l'application m'affiche tous les produits correspondant à ma recherche.
        """
        userQuery = 'nutella'
        apiQuery = [{'product_name_fr': 'Nutella', 'code': '3017620429484', 'nutrition_grade_fr': 'e', 'categories_hierarchy': ['fr:pates-a-tartiner'], 'categories': 'Desayunos,Untables,Untables dulces,Cremas para untar,Cremas de chocolate,Cremas a base de avellanas,Cremas de cacao y avellanas,Pâtes à tartiner', 'image_small_url': 'https://static.openfoodfacts.org/images/products/301/762/042/9484/front_fr.147.200.jpg'}]


        response = self.client.post(reverse('product select'), {'apiQuery': apiQuery, 'userQuery' : userQuery})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'substitution_app/product_select.html')
        self.assertContains(response, "nutella")
        self.assertContains(response, "3017620429484")
        self.assertContains(response, "e")

    def test_safe_products_display(self):
        """
        As Lily, when I chose the exact product to replace, I expect the application to offer me a new page of healthy products.
        En tant que Lily, quand j'ai choisi précisément le produit a substituer, 
        je m'attends à ce que l'application me propose une nouvelle page de produits sains.
        """
        database = ProductsA.objects.create(
                code = '3017620429484',
                url = 'https://uneurl',
                product_name = 'Nutella',
                nutrition_grade_fr = 'e',
                main_category = ['fr:pates-a-tartiner'],
                main_category_fr = 'Pâtes à tartiner',
                image_small_url = 'https://static.openfoodfacts.org/images/products/301/762/042/9484/front_fr.147.200.jpg'
            )
        response = self.client.get(reverse('results', kwargs={'code': '3017620429484'}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ProductsA.objects.all().exists())

    def test_product_display_page(self):
        """
        By clicking on a product, the app displays a product detail page with a link to the Open Food Facts website.
        En cliquant sur un produit, l'application affiche une page de détail du produit 
        comportant un lien vers le site d'Open Food Facts.
        """
        response = self.client.get(reverse('product display', kwargs={'code': '3017620429484'}))
        self.assertEqual(response.status_code, 200)
    
    def test_my_account(self):
        """
        As Lily, I must be able to have space account.
        En tant que Lily, je dois pouvoir avoir un espace compte.
        """
        logged = self.client.login(username='usertest', password='usertest')
        if logged:
            response = self.client.get(reverse('my account'))
            self.assertEqual(response.status_code, 200)
            self.client.logout()
            self.assertTrue(User.objects.filter(username=self.username, email=self.email).exists())
    
    def test_my_products(self):
        """
        As Lily, I need to have access to a summary of all the products I have already substituted.
        En tant que Lily, je dois pouvoir avoir accès à un récapitulatif de tous les produits que j'ai déjà substitué.
        """
        database = UserProducts.objects.create(
                code = '3017620429484',
                url = 'https://uneurl',
                product_name = 'Nutella',
                nutrition_grade_fr = 'e',
                main_category = ['fr:pates-a-tartiner'],
                main_category_fr = 'Pâtes à tartiner',
                image_small_url = 'https://static.openfoodfacts.org/images/products/301/762/042/9484/front_fr.147.200.jpg'
            )
        logged = self.client.login(username='usertest', password='usertest')
        if logged:
            response = self.client.get(reverse('my products'))
            self.assertEqual(response.status_code, 200)
            self.client.logout()
            self.assertTrue(UserProducts.objects.all().exists())
