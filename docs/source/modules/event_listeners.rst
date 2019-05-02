Event Listeners
===============

One common use case for the Paperless Parts SDK is handling resources locally when events happen on the Paperless Part platform. To accommodate this, the Paperless SDK comes with easy to implement event processing capabilities.


Basic Usage
-----------
The Paperless SDK ships with two classes for encapsulating on event processing capabilities: the PaperlessSDK and the ResourceListener specific to the resource you are trying to handle events for.

The general strategy for setting up an on event listener program is:

1. Subclass the ResourceListener for the resource you are tracking events for. (see available ResourceListeners below)
2. Implement the on_event method for your subclassed listener.
3. Instantiate your subclassed resource listener with the configs appropriate for your use case (see configuring your listener instance below)
4. Instantiate a version of the PaperlessSDK.
5. Register your listener to PaperlessSDK.
6. Run the SDK.

**Note: You will have to configure the Paperless SDK Client before running the listener program.**

See the following example:

.. code-block:: python

    from paperless.client import PaperlessClient
    from paperless.main import PaperlessSDK
    from paperless.listeners import OrderListener

    PaperlessClient(...)

    # Step 1
    class MyOrderListener(OrderListener):
        def on_event(self, resource):
            # Step 2
            print("on event")
            print(resource)
            print(resource.to_dict())

    # Step 3
    my_order_listener_instance = MyOrderListener(last_updated=None)

    # Step 4
    my_sdk = PaperlessSDK()

    # Step 5
    my_sdk.add_listener(my_order_listener_instance)

    # Step 6
    my_sdk.run()

Configuring your Listener Instance
----------------------------------
When you instantiate your listener you configure what defines a new resource. That is, you get to draw the line so that all resources pass this one will trigger the on_event method.

Because listeners come with built in caching, you get to draw this line the **first time** you instantiate a subclass of a specific ResourceListener. There are two ways to do this:

1. You can pass in the unique identifier of the last resource of that type you have processed as the last_updated param. By passing in a value as the last_updated param you are telling the listener to trigger the on_event method for all **future** resources **not including** the resource whose identifier you passed.
2. You can choose not to pass a last_updated param. Not passing a last_updated param will result in the listener finding the last updated resource in Paperless Parts and then using that as the starting point so that on_event will only be triggered for resources created after the moment you instantiate your listener.

**Note: You can run into a weird situation if you choose not to pass in a last_updated, do not have any Paperless resources for the resource you are listening for, and have requested from Paperless to initiaite your resource at a specific index (for instance requested a specific order or quote number).**

Paperless resource listeners will cache all successfully processed resources. When re-initiating or re-starting your program, you will start off right where you left off.

TODO: ADD A WAY TO CLEAR THE CACHE AND DOCUMENT THAT HERE


Available Resource Listeners
----------------------------
.. autoclass:: paperless.listeners.OrderListener
    :members: on_event
    :undoc-members:
    :show-inheritance: