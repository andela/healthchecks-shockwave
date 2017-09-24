'''Consume the shopify webhook API'''
import json
from django.conf import settings
import requests
from hc.api.models import Integration

class ShopifyMessages():
    '''A class that adds a shopify webhook, deletes a shopify webhook and
    returns a shopify webhook.
    '''
    def add_shopify_webhook_check(self, event, check_code, url):
        '''Add webhook to client's shopify account
        Keyword Arguments:
        event -- The type of event to which a check is added
        check_code -- The check code to be added
        url -- The store's url
        '''
        site_root = settings.SITE_ROOT
        if site_root == "http://localhost:8000":
            site_root = "https://myhealthcheckskite.pagekite.me/"
        raw_data = {
            "webhook": {
                "topic": event,
                "address": site_root + "ping/" +str(check_code),
                "format": "json"
                }
        }
        json_data = json.dumps(raw_data)
        webhook_url = url + "/admin/webhooks.json"
        store = Integration.objects.filter(value_store=url).first()
        post_webhook = requests.post(webhook_url, data=json_data,
                                     auth=requests.auth.HTTPBasicAuth(store.value_api_key,
                                                                      store.value_store_password),
                                     headers={"Content-type": "application/json"})
        print(post_webhook.content)

    def get_shopify_webhooks(self, url):
        '''Return webhooks for a client's shopify account
        Keyword Argument:
        url -- The store's url
        '''
        webhook_url = url + "/admin/webhooks.json"
        store = Integration.objects.filter(value_store=url).first()
        get_webhooks = requests.get(webhook_url,
                                    auth=requests.auth.HTTPBasicAuth(store.value_api_key,
                                                                     store.value_store_password))
        return get_webhooks.content

    def delete_webhook(self, webhook_id, url):
        '''Delete webhook from shopify account
        Keyword Argument:
        webhook_id -- The id of the webhook to be deleted
        url -- The store's url
        '''
        webhook_url = url + "/admin/webhooks/" + webhook_id + ".json"
        store = Integration.objects.filter(value_store=url).first()
        requests.delete(webhook_url,
                        auth=requests.auth.HTTPBasicAuth(store.value_api_key,
                                                         store.value_store_password))
                                                                 