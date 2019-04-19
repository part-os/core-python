from paperless.client import PaperlessClient
from paperless.main import PaperlessSDK
from paperless.listeners import OrderListener

class MyOrderListener(OrderListener):
    def on_event(self, resource):
        print("on event")
        print(resource)


my_order_listener = MyOrderListener(last_updated=49) #Challenge, how does one turn this on and off without passing in this number?
my_client = PaperlessClient(username='', password='', group_slug='', version=PaperlessClient.VERSION_0)
my_sdk = PaperlessSDK(my_client)
my_sdk.add_listener(my_order_listener)
my_sdk.run()
