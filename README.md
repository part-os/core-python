# Part OS Paperless Parts SDK (Python)
The Paperless Parts Software Development Kit (SDK) enables developers to easily write custom event listeners 
for object created events from the Paperless Parts web application.

## Prerequisites

Install the required Python packages:
```
cd path\to\core-python
pip install -r requirements.txt
```

## Authenticating the client
To authenticate your client you will need to instantiate your client from paperless/client with
1. username = your paperless email login
2. password = the password to your paperless account
3. group_slug = the slug associated with your supplier user group

## Writing custom listeners 

Writing a custom listener involves extending an object listener from paperless/listeners and overwriting its on_event method with your custom
logic.


### CAUTION
Once registered, your custom on_event method will be hit repeatedly until it finishes successfully.
If your listener is unable to succeed, it means that your program will get 'stuck' on that resource and will never be able to move on to other ones. 
It is the responsibility of the listener subclass to handle exceptions.

## Instantiating your listener
The first time you run the Paperless SDK you will have the option of configuring which resource to set as your baseline. 
The baseline resource, will NOT be handled by your custom listener, but all subsequent resources after it will trigger your custom
on_event logic. Configuring the base resource is done by passing its number, such as an order number, as the last_updated param when
instantiating the listener.

If you choose not to pass in a baseline resource, then the baseline will be set to the latest resource and your custom on_event logic will
be applied to all new resources.

## Registering your listener and running the SDK

The PaperlessSDK is found in paperless/main and is event driven. It has two methods add_listener and run. 
add_listener() accepts an insance of a class that extends the BaseListener class and implements the on_event method.
run() begins the execution of the PaperlessSDK.

After you have writen your custom listener class and instantiated it, you can register it with the add_listener method and start the SDK
with the run() method.

## Example

```
from paperless.client import PaperlessClient
from paperless.main import PaperlessSDK
from paperless.listeners import OrderListener

class MyOrderListener(OrderListener):
    def on_event(self, resource):
        print("on event")
        print(resource)


my_client = PaperlessClient(username='', password='', group_slug='', version=PaperlessClient.VERSION_0)
my_order_listener = MyOrderListener(client=my_client, last_record_id=None)
my_sdk = PaperlessSDK()
my_sdk.add_listener(my_order_listener)
my_sdk.run()
```
