'''Test the addition of shopify a third party application integration.
'''
from hc.api.models import Integration
from hc.test import BaseTestCase

class AddShopifyIntegration(BaseTestCase):
    '''Test the addition of a shopify store and the validation
    of a shopify url.
    '''
    def test_it_adds_shopify(self):
        '''Test the successful additon of a shopify
        account by passing in valid data that should redirect the
        page and increase the count of integrations.
        '''
        url = "/integrations/add_integration/"
        form = {"integration_name": "shopify",
                "value_store": "https://examplestore.myshopify.com",
                "value_api_key": "examplestring",
                "value_store_password":"examplestring"}
        self.client.login(username="alice@example.org", password="password")
        post_shopify_store = self.client.post(url, form)
        self.assertRedirects(post_shopify_store, "/integrations/")
        self.assertEqual(Integration.objects.count(), 1)

    def test_it_validates_urls(self):
        '''Test the validaiton of urls by passing in an invalid url
        that leads to an error message prompt and no addition of integrations.
        '''
        url = "/integrations/add_integration/"
        form = {"integration_name": "shopify",
                "value_store": "wrong_url_input",
                "value_api_key": "examplestring",
                "value_store_password":"examplestring"}
        self.client.login(username="alice@example.org", password="password")
        post_shopify_store = self.client.post(url, form)
        self.assertContains(post_shopify_store, "Enter a valid URL", status_code=200)
        self.assertEqual(Integration.objects.count(), 0)
