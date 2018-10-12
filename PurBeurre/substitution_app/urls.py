from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home page'),
    path('signup/', views.signup, name='sign up'),
    path('connection/', views.connection, name='connection'),
    path('deconnection/', views.deconnection, name='deconnection'),
    path('myaccount/', views.myaccount, name='my account'),
    path('product_select/', views.product_select, name='product select'),
    path('results/<int:code>', views.results, name='results'),
    path('product_display/<int:code>', views.product_display, name='product display'),
    path('myproducts/', views.my_products, name='my products'),
    path('noSubProdFound/', views.results, name='no Substitute'),
    path('noProdFound/', views.product_select, name='no product found'),
    path('LegalNotice/', views.LegalNotice, name='Legal Notice'),

]