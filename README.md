Part OS Paperless Parts SDK (Python)
====================================

The [Paperless Parts](https://www.paperlessparts.com) Software Development Kit 
(SDK) enables developers to easily write custom event listeners that run when 
objects are created in Paperless Parts. The most common use case is creating 
orders and other records in an ERP system after an order is placed in Paperless 
Parts. The SDK uses the 
[Paperless Parts Open API](https://docs.paperlessparts.com) to access your 
data.

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
your Paperless Parts account. To generate, revoke, or re-generate this token, 
go to Settings > Integrations > API Token. This token must be included in the 
header of all requests using the key as follows:

`Authorization`: `API-Token <api-token>` 

The SDK handles this for you when you this access token when instantiating your 
`PaperlessClient` object, as shown in the example below. We recommend 
structuring your application to read this from a configuration file. Your access 
token should never be committed to your version control system (like git).


Writing custom listeners
------------------------ 

The SDK provides the `paperless.listeners.BaseListener` class, which can be 
extended to listen for particular object creation event. The subclass
`paperless.listeners.OrderListener` is provided to listen for new order creation 
events. You can extend `OrderListener` and implement an `on_event` method. Similary,
`paperless.listeners.QuoteListener` is provided to listen for new quotes.

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

    class MyQuoteListener(QuoteListener):
        def on_event(self, resource):
            print("on event")
            print(resource)
    
    my_client = PaperlessClient(access_token='', version=PaperlessClient.VERSION_0)
    my_order_listener = MyOrderListener(last_record_id=None)
    my_quote_listener = MyQuoteListener(last_record_id=None)
    my_sdk = PaperlessSDK()
    my_sdk.add_listener(my_order_listener)
    my_sdk.add_listener(my_quote_listener)
    my_sdk.run()


Custom Tables
-------------

In Paperless Parts, you can upload and manage custom user-defined tables. With
custom tables, you can perform table lookups from within your customized pricing
logic. This section will demonstrate how to create and manage custom tables from
the SDK.

First, import the `CustomTable` class:
```python
from paperless.custom_tables.custom_tables import CustomTable
```

Next, list all of the tables in your account:
```python
CustomTable.get_list()
```

A custom table is defined by two things: its configuration and its row data. The
configuration defines the table's column names and types, and the row data provides
the contents of the table's rows.

To create and populate a table, first instantiate a `CustomTable` with a
configuration, or a configuration and accompanying row data. The configuration
should be a list of dictionaries with keys `'column_name'` and `'value_type'`,
and optionally `'is_for_unique_key'` (more on this later). The allowed value
types are: string, numeric, boolean. The row data should be a list of
dictionaries with keys corresponding to the column names supplied in the
configuration.

```python
sample_table_config = [
    dict(column_name='diameter', value_type='numeric'),
    dict(column_name='length', value_type='numeric'),
    dict(column_name='requires_prep', value_type='boolean'),
    dict(column_name='material', value_type='string'),
]
sample_table_rows = [
    dict(diameter=1.0, length=24.0, requires_prep=False, material='6061-T6'),
    dict(diameter=2.0, length=48.0, requires_prep=False, material='5052-H32'),
    dict(diameter=3.0, length=24.0, requires_prep=True, material='304-2B'),
    dict(diameter=4.0, length=48.0, requires_prep=True, material='304-#4'),
    dict(diameter=5.0, length=24.0, requires_prep=True, material='Ti6Al4V'),
    dict(diameter=6.0, length=48.0, requires_prep=False, material='A2'),
]

table = CustomTable(config=sample_table_config, data=sample_table_rows)
```

You may supply a configuration without row data, but any row data supplied must be
accompanied by a configuration.

In order to create this table you've defined in Paperless Parts, first `create` the
table, supplying a table name, and then call `update`.
```python
table.create('test_sdk_table_1')  # This creates a blank new table
table.update('test_sdk_table_1')  # This populates the table with the supplied config and data
```

NOTE: When you call `update` on a table, you will blow away whatever config and data
were there before and replace them with the new config and data you've supplied.

You can also instantiate a table from a configuration CSV file, or a combination of a
configuration CSV file and a data CSV file. Here are some example CSV file contents
corresponding to the Python examples above:

config.csv
```
column_name,value_type
diameter,numeric
length,numeric
requires_prep,boolean
material,string
```

data.csv
```
diameter,length,requires_prep,material
1,24,FALSE,6061-T6
2,48,FALSE,5052-H32
3,24,TRUE,304-2B
4,48,TRUE,304-#4
5,24,TRUE,Ti6Al4V
6,48,FALSE,A2
```

To instantiate a `CustomTable` from CSV files, do the following:
```python
table = CustomTable()
table.from_csv('config.csv', 'data.csv')
```

You can also download the CSV files for the table config and data using the
`download_csv` method, providing the table name as an argument. This can be useful
if you want to modify the existing data in the table slightly. Supply
`config=True` if you want the config file. You can also supply an optional
`file_path` argument to specify where to save the file to:
```python
CustomTable.download_csv('test_sdk_table_1')  # download the data file
CustomTable.download_csv('test_sdk_table_1', config=True)  # download the config file
CustomTable.download_csv('test_sdk_table_1', file_path='renamed_test_sdk_table_1_data.csv')  # download the data file and rename it
```

You can delete a `CustomTable` from your Paperless Parts account by calling
the `delete` method with the table's name:
```python
CustomTable.delete('test_sdk_table_1')
```

Changing Quote Status
---------------------

You can change a quote's status using the `set_status` method. The available statuses 
are `OUTSTANDING`, `CANCELLED`, `TRASH`  `LOST`, these statuses are defined in the `STATUSES`
enum on the `Quote` object.

Example:

```python
quote = Quote.get(1090)
quote.set_status(Quote.STATUSES.OUTSTANDING)
```
