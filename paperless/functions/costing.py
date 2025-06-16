from typing import Optional

from paperless.client import PaperlessClient
from paperless.functions.components import _quote_item_base_url
from paperless.objects.quotes import QuoteComponent

_bulk_costing_update_limit = 100


def update_component_costing_variables(
    quote_item_id: int, qc: QuoteComponent, client: Optional[PaperlessClient] = None
):
    '''Update the costing variables for a component. Does not recalculate the total amount on a quote'''
    target_url = f'{_quote_item_base_url}/items/{quote_item_id}/bulk_costing'
    api_handle = client if client is not None else PaperlessClient.get_instance()
    payload = qc.get_costing_updates()
    if len(payload) > _bulk_costing_update_limit:
        raise ValueError(
            f'quote component {qc.id} has more than {_bulk_costing_update_limit} updates'
        )
    # we will throw on any error condition, the API will return 204 on a success
    _ = api_handle.request(
        target_url, method=PaperlessClient.METHODS.PATCH, data=payload
    )
