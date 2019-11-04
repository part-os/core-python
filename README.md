Part OS Paperless Parts SDK (Python)
====================================

The [Paperless Parts](https://www.paperlessparts.com) Software Development Kit 
(SDK) enables developers to easily write custom event listeners that run when 
objects are created in Paperless Parts. The most common use case is creating 
orders and other records in an ERP system after an order is placed in Paperless 
Parts.

Prerequisites
-------------

These instructions assume you are running on Windows 10.

First install the latest [Python3](https://www.python.org/downloads/), which 
includes `python3`, `pip`, and `venv`. Add the Python installation folder to 
your system path. 

Create a virtual environment and activate it:

    python -m venv osenv
    osenv\Scripts\activate

Install the required Python packages:

    cd path\to\core-python
    pip install -r requirements.txt

Make sure `paperless` is on your Python path. You can do this using an 
environment variable like this:

    set PYTHONPATH=c:\path\to\core-python


Authenticating the client
-------------------------

The SDK client is authenticated via an automatically generated token linked to 
your Paperless Parts account. For instructions on how to obtain, revoke, and 
re-create this token, please contact support@paperlessparts.com. You provide 
this access token when instantiating your `PaperlessClient` object, as shown in 
the example below. We recommend structuring your application to read this from
a configuration file. Your access token should never be committed to your 
version control system (like git).


Writing custom listeners
------------------------ 

The SDK provides the `paperless.listeners.BaseListener` class, which can be 
extended to listen for particular object creation event. The subclass
`paperless.listeners.OrderListener` is provided to listen for new order creation 
events. You can extend `OrderListener` and implement an `on_event` method. Similary,
`paperless.listeners.QuoteListener` is provided to listen for new quote creation.

You will need to handle all exceptions if you intend to have a long-running 
listener that does not require manual restarts. Alternatively, you can add
watchdog or restart logic to your application built on the SDK. 


Instantiating your listener
---------------------------

Listeners keep track of which objects they have processed and persist this
data in a local file in JSON format.

The first time you run the Paperless SDK you can optionally configure the 
listener to start with a later object (for example, an order with number other 
than 1) by providing `last_record_id` when instantiating the listener.
`last_record_id` represents the last record that was processed, and this record
will not be processed. Once resources have been processed and the local JSON 
file has been initialized, the `last_record_id` will be ignored.


Registering your listener and running the SDK
---------------------------------------------

The `paperless.main.PaperlessSDK` class provides the event loop to regularly 
check for new objects and call any registered listeners. Use the `add_listener`
to register your listener subclass and `run` to start the event loop. You can 
customize the polling interval (in seconds) by specifying the `delay` argument
when instantiating `PaperlessSDK`. The default and recommended delay is 900 
seconds (15 minutes).

By default, the event loop will run until the program is terminated. If you 
wish to manage these intervals elsewhere in your application, set `loop=False`
when instantiating `PaperlessSDK`, which cause `run()` to check for objects one
time and then return.    


Example
-------

    from paperless.client import PaperlessClient
    from paperless.main import PaperlessSDK
    from paperless.listeners import OrderListener
    
    class MyOrderListener(OrderListener):
        def on_event(self, resource):
            print("on event")
            print(resource)

    class MyQuoteListner(QuoteListener):
        def on_event(self, resource):
            print("on event")
            print(resource)
    
    my_client = PaperlessClient(access_token='', version=PaperlessClient.VERSION_0)
    my_order_listener = MyOrderListener(client=my_client, last_record_id=None)
    my_quote_listener = MyQuoteListener(client=my_client, last_record_id=None)
    my_sdk = PaperlessSDK()
    my_sdk.add_listener(my_order_listener)
    my_sdk.add_listener(my_quote_listener)
    my_sdk.run()
