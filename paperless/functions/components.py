from typing import List

from paperless.client import PaperlessClient
from paperless.objects.quotes import QuoteComponent
from paperless.objects.utils import safe_init


def GetQuoteItemComponents(
    quote_item_id: int, start_at: int = 1
) -> List[QuoteComponent]:
    '''eagerly gets all components from a quote item, working through all pages'''
    if start_at < 1:
        raise ValueError('invalid starting point')
    comps: list[QuoteComponent] = []
    client = PaperlessClient.get_instance()
    params = {}
    if start_at != 1:
        params['page'] = start_at
    component_url = f'quote-items/{quote_item_id}/components/'
    try:
        json_objs = []
        res = client.get_resource_list(component_url, params)
        json_objs.extend(res['results'])
        while res.get('next') is not None:
            next = res['next']
            res = client.get_resource_list(next)
            json_objs.extend(res['results'])
        for obj in json_objs:
            comps.append(safe_init(QuoteComponent, obj))
        return comps
    except Exception as e:
        raise e
