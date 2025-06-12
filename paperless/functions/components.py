from typing import Any, Dict, List, Optional

from paperless.client import PaperlessClient
from paperless.objects.quotes import QuoteComponent, QuoteItem
from paperless.objects.utils import safe_init

_quote_item_base_url = 'v1/quotes/public/'


def get_quote_item_components(
    quote_item_id: int, start_at: int = 1, client: Optional[PaperlessClient] = None
) -> List[QuoteComponent]:
    '''eagerly gets all components from a quote item, working through all pages'''
    api_handle = client if client is not None else PaperlessClient.get_instance()
    if start_at < 1:
        raise ValueError('invalid starting point')
    comps: list[QuoteComponent] = []
    params = {}
    if start_at != 1:
        params['page'] = start_at
    component_url = f'{_quote_item_base_url}/items/{quote_item_id}/components/'
    json_objs = _retrieve_paginated_data(component_url, params, api_handle)
    for obj in json_objs:
        comps.append(safe_init(QuoteComponent, obj))
    return comps


def get_quote_items(
    quote_id: int, start_at: int = 1, client: Optional[PaperlessClient] = None
) -> List[QuoteItem]:
    '''eagerly get all quote-items from a quote, working through all pages
    IMPORTANT NOTE: The API endpoint this function uses will not return
    QuoteComponents! It will return the QuoteComponent ids, however, so
    individual components can be retrieved later.
    '''
    api_handle = client if client is not None else PaperlessClient.get_instance()
    if start_at < 1:
        raise ValueError('invalid starting point')
    comps: list[QuoteItem] = []
    params = {}
    if start_at != 1:
        params['page'] = start_at
    target_url = f'{_quote_item_base_url}/{quote_id}/items/'  # yes, very similar but not the same as above
    json_objs = _retrieve_paginated_data(target_url, params, api_handle)
    for obj in json_objs:
        # add an empty collection of QuoteComponents to keep safe_init happy
        obj['components'] = []
        comps.append(safe_init(QuoteItem, obj))
    return comps


def _retrieve_paginated_data(
    target_url: str,
    params: Dict[str, Any],
    client: PaperlessClient,
) -> List[Dict[str, Any]]:
    json_objs = []
    res = client.get_resource_list(target_url, params)
    json_objs.extend(res['results'])
    while res.get('next') is not None:
        next = res['next']
        res = client.get_resource_list(next)
        json_objs.extend(res['results'])
    return json_objs
