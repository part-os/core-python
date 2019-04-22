from paperless.client import PaperlessClient
from paperless.main import PaperlessSDK
from paperless.listeners import OrderListener

class MyOrderListener(OrderListener):
    def on_event(self, resource):
        print("on event")
        print(resource)


my_client = PaperlessClient(username='', password='', group_slug='', version=PaperlessClient.VERSION_0)
my_order_listener = MyOrderListener(client=my_client, last_updated=None)
my_sdk = PaperlessSDK()
my_sdk.add_listener(my_order_listener)
my_sdk.run()
