from typing import Dict, Optional, Union

from paperless.client import PaperlessClient
from paperless.functions.components import _quote_item_base_url
from paperless.objects.quotes import (
    CostingVariablePayload,
    QuoteComponent,
    QuoteCostingVariable,
    QuoteCostingVariableMixin,
)

_bulk_costing_update_limit = 100

SingleValueType = Union[float, int, str, bool]
RowType = Dict[str, SingleValueType]
QuantitySpecificRowType = Dict[int, RowType]
QuantitySpecificValueType = Dict[int, SingleValueType]


# Convert a table-type QuoteCostingVariable to the required payload for a costing update
def _table_update_transform(
    v: QuoteCostingVariable,
) -> Union[RowType, QuantitySpecificRowType]:
    if v.variable_class != 'table':
        raise ValueError(f'{v.label} is of type {v.variable_class}, not "table"')
    if v.quantity_specific is True:
        q_dict = {}
        for k, cvp in v.quantities.items():
            q_dict[k] = cvp.row if cvp.row is not None else {}
        return q_dict
    else:
        # table variables have a single quantity of 1 if it's not quantity-specific
        cvp = v.quantities[1]
        return cvp.row if cvp.row is not None else {}


def _variable_update_transform(
    v: QuoteCostingVariable,
) -> Union[SingleValueType, QuantitySpecificValueType]:
    if v.variable_class != 'basic' and v.variable_class != 'drop_down':
        raise ValueError(f'{v.label} is of unsupported type {v.variable_class}')
    if v.quantity_specific is True:
        q_dict = {}
        for k, cvp in v.quantities.items():
            q_dict[k] = cvp.value
        return q_dict
    else:
        return v.value


def get_costing_variable_updates(
    mixin_object: QuoteCostingVariableMixin,
) -> Dict[str, Dict]:
    """
    Generate costing updates for a QuoteCostingVariableMixin object.

    Args:
        mixin_object: An object that has a costing_variables field (e.g. operations, add-ons, pricing items)

    Returns:
        Dictionary containing the costing variable updates organized by type
    """
    dd_vars = {}
    t_vars = {}
    vars = {}
    for cv in mixin_object.costing_variables:
        if cv.variable_class == 'drop_down':
            dd_vars[cv.label] = _variable_update_transform(cv)
        elif cv.variable_class == 'table':
            t_vars[cv.label] = _table_update_transform(cv)
        else:
            vars[cv.label] = _variable_update_transform(cv)

    all_vars = {}
    if len(dd_vars) > 0:
        all_vars['drop_down_variables'] = dd_vars
    if len(t_vars) > 0:
        all_vars['table_variables'] = t_vars
    if len(vars) > 0:
        all_vars['variables'] = vars
    return all_vars


def get_component_costing_updates(component: QuoteComponent) -> Dict[int, Dict]:
    """
    Generate a payload for bulk-update of all operation costing variables for a component.

    Args:
        component: The QuoteComponent to generate costing updates for

    Returns:
        Dictionary mapping operation IDs to their costing update payloads
    """
    vars = {}
    for mop in component.material_operations:
        vars[mop.id] = get_costing_variable_updates(mop)
    for sop in component.shop_operations:
        vars[sop.id] = get_costing_variable_updates(sop)
    return vars


def update_component_costing_variables(
    quote_item_id: int, qc: QuoteComponent, client: Optional[PaperlessClient] = None
):
    '''Update the costing variables for a component. Does not recalculate the total amount on a quote'''
    target_url = f'{_quote_item_base_url}/items/{quote_item_id}/bulk_costing'
    api_handle = client if client is not None else PaperlessClient.get_instance()
    payload = get_component_costing_updates(qc)
    if len(payload) > _bulk_costing_update_limit:
        raise ValueError(
            f'quote component {qc.id} has more than {_bulk_costing_update_limit} updates'
        )
    # we will throw on any error condition, the API will return 204 on a success
    _ = api_handle.request(
        target_url, method=PaperlessClient.METHODS.PATCH, data=payload
    )
