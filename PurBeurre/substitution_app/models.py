from django.db import models


class ProductsA(models.Model):
    code = models.BigIntegerField(primary_key=True)
    url = models.CharField(max_length=250)
    product_name = models.CharField(max_length=250)
    nutrition_grade_fr = models.CharField(max_length=1)
    main_category = models.CharField(max_length=250)
    main_category_fr = models.CharField(max_length=250)
    image_small_url = models.CharField(max_length=250)

    class Meta:
        verbose_name = "Produits A"
        managed = False
        db_table = 'products_A'
    
    def __str__(self):
        return self.product_name


class UserProducts(models.Model):
    username = models.CharField(max_length=150)
    code = models.BigIntegerField()
    url = models.CharField(max_length=250)
    product_name = models.CharField(max_length=250)
    nutrition_grade_fr = models.CharField(max_length=1)
    main_category = models.CharField(max_length=250)
    main_category_fr = models.CharField(max_length=250)
    image_small_url = models.CharField(max_length=250)

    class Meta:
        verbose_name = "Produits utilisateur"
        managed = False
        db_table = 'user_products'

    def __str__(self):
        return self.product_name