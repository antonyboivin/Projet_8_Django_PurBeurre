#!/usr/bin/env python3
"""
    The callapi module handles all interactions between the application and the OFF API.
"""
import json
import requests

from django.http import Http404


class Callapi():
    """
        Class Callapi groups the methods necessary to interact with the OFF API.
    """
    def request_the_openfoodfact_api(self, query):
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

        except requests.exceptions.HTTPError as err:
            return response.status_code


    def clean_the_openfoodfact_api_request(self, response):
        """
            Analyze the response of the API to keep only the useful information.
        """
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

    def barcode_request_the_openfoodfact_api(self, barcode):
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


    def barcode_clean_the_oppenfoodfact_api_request(self, response):
        """
            Analyze the response of the API to keep only the useful information.
        """
        results = []
        products = {}
        try:
            items = response["product"]
            products["product_name_fr"] = items["product_name_fr"]
            products["code"] = items["code"]
            products["nutrition_grade_fr"] = items["nutrition_grade_fr"]
            products["categories_hierarchy"] = [categorie for categorie in \
                            items["categories_hierarchy"] if categorie[0:2] == 'fr']
            products["categories"] = items["categories"]
            products["image_small_url"] = items["image_small_url"]

            results.append(products.copy())
            results = results[0]

        except KeyError:
            raise Http404

        return results


    def request_for_substitution_products_in_openfoodfact_api(self, apiquery):
        """
            Queries the API with filters such as the natural score
            to find substitutes in the same product category of the user's request.
        """

        url = 'https://fr.openfoodfacts.org/cgi/search.pl'
        # Determinations of the build parameters of the query.
        payload = {
            'action' : 'process',
            'search_terms' : apiquery["categories_hierarchy"][0][3:],
            # First criteria
            'tagtype_0' : 'nutrition_grades',
            'tag_contains_0':'contains',
            'tag_0' : 'a',
            # Third criteria
            'tagtype_1' : 'nutrition_grades',
            'tag_contains_1':'contains',
            'tag_1' : 'b',

            'sort_by' : 'unique_scans_n',
            'json' : '1',
            'page_size' : 100,
            'page' : '1'
        }

        # Built of the query
        try:
            response = requests.get(url, params=payload)
            requests.get(url, params=payload).raise_for_status()
            #return response.json()
            return(response.json())
        except requests.exceptions.HTTPError as err:
            return response.status_code


    def clean_substitution_products_in_openfoodfact_api(self, apiquery):
        """
            Analyze the response of the API to keep only the useful information.
        """
        results = []
        products = {}
        count = apiquery["count"]
        if count > 0:
            items = apiquery["products"]

            for item in items:
                try:
                    products["product_name"] = item["product_name_fr"]
                    products["code"] = item["code"]
                    products["nutrition_grade_fr"] = item["nutrition_grade_fr"]
                    products["categories_hierarchy"] = [categorie for categorie in \
                                    item["categories_hierarchy"] if categorie[0:2] == 'fr']
                    products["categories"] = item["categories"]
                    products["image_small_url"] = item["image_small_url"]

                    if len(products["categories"]) > 0:
                        results.append(products.copy())

                except KeyError:
                    pass

            if len(results) > 0:
                return results
            else:
                raise Http404
