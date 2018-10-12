import json
import requests


def request_the_openfoodfact_api(query):
    """
        Build the query to query the API with the user's request.
    """
    url = 'https://fr.openfoodfacts.org/cgi/search.pl'
    # Determinations of the build parameters of the query.
    payload = {
        'search_terms' : query,
        'search_simple' : 1,
        'action' : 'process',
        'json' : '1',
        'page_size' : 100,
        'page' : '1'
    }
    # Built of the query
    try:
        response = requests.get(url, params=payload)
        requests.get(url, params=payload).raise_for_status()
        return response.json()
        #return response.url

    except requests.exceptions.HTTPError as err:
        return response.status_code


def clean_the_openfoodfact_api_request():

    response = {
                    "products": [
                        {
                            "image_small_url": "https://static.openfoodfacts.org/images/products/301/762/042/9484/front_fr.147.200.jpg",
                            "categories": "Petit-d\u00e9jeuners,Produits \u00e0 tartiner,Produits \u00e0 tartiner sucr\u00e9s,P\u00e2tes \u00e0 tartiner,P\u00e2tes \u00e0 tartiner au chocolat,P\u00e2tes \u00e0 tartiner aux noisettes,P\u00e2tes \u00e0 tartiner aux noisettes et au cacao",
                            "product_name_fr": "Nutella",
                            "code": "3017620429484",

                            "categories_hierarchy": [
                                "en:breakfasts",
                                "en:spreads",
                                "en:sweet-spreads",
                                "fr:pates-a-tartiner",
                                "en:chocolate-spreads",
                                "en:hazelnut-spreads",
                                "en:cocoa-and-hazelnuts-spreads"
                            ],
                            "nutrition_grade_fr": "e",
                        },
                        {
                            "image_small_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.200.jpg",
                            "categories": "Produits \u00e0 tartiner,Petit-d\u00e9jeuners,Produits \u00e0 tartiner sucr\u00e9s,P\u00e2tes \u00e0 tartiner,P\u00e2tes \u00e0 tartiner au chocolat,P\u00e2tes \u00e0 tartiner aux noisettes,P\u00e2tes \u00e0 tartiner aux noisettes et au cacao,P\u00e2tes \u00e0 tartiner",
                            "product_name_fr": "Nutella",            
                            "code": "3017624047813",

                            "categories_hierarchy": [
                                "en:breakfasts",
                                "en:spreads",
                                "en:sweet-spreads",
                                "fr:pates-a-tartiner",
                                "en:chocolate-spreads",
                                "en:hazelnut-spreads",
                                "en:cocoa-and-hazelnuts-spreads"
                            ],
                            "nutrition_grade_fr": "e",
                        },
                                ],
                    "count": 2,
                    "skip": 0,
                    "page_size": "100",
                    "page": 1
                }
    results = []
    products = {}
    count = response["count"]
    if count > 0:
        items = response["products"]
        for item in items:
            try:
                products["product_name"] = item["product_name_fr"]
                products["code"] = item["code"]
                products["nutrition_grade_fr"] = item["nutrition_grade_fr"]
                products["categories_hierarchy"] = [categorie for categorie in \
                                item["categories_hierarchy"] if categorie[0:2] == 'fr']
                products["categories"] = item["categories"]
                products["image_small_url"] = item["image_small_url"]

                if len(products["categories"]) > 0 and \
                                len(products["categories_hierarchy"]) > 0:
                    results.append(products.copy())

            except KeyError:
                pass

        return results
    else:
        return None



def barcode_request_the_openfoodfact_api(barcode):
    """
        Build the query to query the API with a bar code.
    """
    url = 'https://world.openfoodfacts.org/api/v0/product/' + str(barcode) + '.json'
    try:
        response = requests.get(url)
        requests.get(url).raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as err:
        return response.status_code

        ###################################
        #            TEST ZONE            #
        ###################################

def test_request_the_openfoodfact_api_response_url():
    query = "pytest"
    assert request_the_openfoodfact_api(query) == "https://fr.openfoodfacts.org/cgi/search.pl?search_terms=pytest&search_simple=1&action=process&json=1&page_size=100&page=1"

def test_request_the_openfoodfact_api_response():
    query = 'nutella'
    assert 'products' in request_the_openfoodfact_api(query)
    assert 'product_name_fr' in request_the_openfoodfact_api(query)['products'][0]
    assert 'image_small_url' in request_the_openfoodfact_api(query)['products'][0]
    assert 'code' in request_the_openfoodfact_api(query)['products'][0]
    assert 'categories_hierarchy' in request_the_openfoodfact_api(query)['products'][0]
    assert 'nutrition_grade_fr' in request_the_openfoodfact_api(query)['products'][0]

def test_clean_the_openfoodfact_api_request():
    response = [
        {'product_name': 'Nutella', 'code': '3017620429484', 'nutrition_grade_fr': 'e', 'categories_hierarchy': ['fr:pates-a-tartiner'], 'categories': 'Petit-déjeuners,Produits à tartiner,Produits à tartiner sucrés,Pâtes à tartiner,Pâtes à tartiner au chocolat,Pâtes à tartiner aux noisettes,Pâtes à tartiner aux noisettes et au cacao', 'image_small_url': 'https://static.openfoodfacts.org/images/products/301/762/042/9484/front_fr.147.200.jpg'}, 
        {'product_name': 'Nutella', 'code': '3017624047813', 'nutrition_grade_fr': 'e', 'categories_hierarchy': ['fr:pates-a-tartiner'], 'categories': 'Produits à tartiner,Petit-déjeuners,Produits à tartiner sucrés,Pâtes à tartiner,Pâtes à tartiner au chocolat,Pâtes à tartiner aux noisettes,Pâtes à tartiner aux noisettes et au cacao,Pâtes à tartiner', 'image_small_url': 'https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.200.jpg'}]
    assert clean_the_openfoodfact_api_request() == response

def test_barcode_request_the_openfoodfact_api():
    barcode = '3017620429484'
    assert 'product' in barcode_request_the_openfoodfact_api(barcode)
    assert 'product_name_fr' in barcode_request_the_openfoodfact_api(barcode)['product']
    assert 'image_small_url' in barcode_request_the_openfoodfact_api(barcode)['product']
    assert 'code' in barcode_request_the_openfoodfact_api(barcode)['product']
    assert 'categories_hierarchy' in barcode_request_the_openfoodfact_api(barcode)['product']
    assert 'nutrition_grade_fr' in barcode_request_the_openfoodfact_api(barcode)['product']