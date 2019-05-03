Authentication
==============

The first step in using the Paperless Parts SDK is to authenticate a client.

Authenticating your client requires having access to a username and password for an account that has been authenticated with the Paperless SDK. To set up one of these accounts, please **contact support@paperlessparts.com**.

Basic Example
-------------

.. code-block:: python

    from paperless.client import PaperlessClient

    # instantiate your client
    PaperlessClient(
        username='',
        password='',
        group_slug='your-slug',
    )

Advanced Usage
--------------
Advanced users have the ability to pass the base_url param when constructing the client. You can use this base url to specify which sandbox account you are testing with. To set up a sandbox account, please **contact support@paperlessparts.com**.

.. code-block:: python

    from paperless.client import PaperlessClient

    # instantiate your client
    PaperlessClient(
        username='',
        password='',
        group_slug='your-slug',
        base_url='you-sandbox',
    )
