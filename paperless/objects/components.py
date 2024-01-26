import collections
from typing import TYPE_CHECKING, Generator, List, NamedTuple, Optional, Union

import attr

from paperless.objects.common import Money
from paperless.objects.utils import convert_cls, convert_iterable, optional_convert

if TYPE_CHECKING:
    from paperless.objects.orders import OrderComponent
    from paperless.objects.quotes import QuoteComponent


@attr.s(frozen=True)
class Material:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    display_name: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    family: str = attr.ib(validator=attr.validators.instance_of(str))
    material_class: str = attr.ib(validator=attr.validators.instance_of(str))
    name: str = attr.ib(validator=attr.validators.instance_of(str))


@attr.s(frozen=True)
class BaseOperation:
    @attr.s(frozen=True)
    class OperationQuantity:
        price: Optional[Money] = attr.ib(
            converter=optional_convert(Money),
            validator=attr.validators.optional(attr.validators.instance_of(Money)),
        )
        manual_price: Optional[Money] = attr.ib(
            converter=optional_convert(Money),
            validator=attr.validators.optional(attr.validators.instance_of(Money)),
        )
        lead_time: Optional[int] = attr.ib(
            validator=attr.validators.optional(attr.validators.instance_of(int))
        )
        manual_lead_time: Optional[int] = attr.ib(
            validator=attr.validators.optional(attr.validators.instance_of(int))
        )
        quantity: int = attr.ib(validator=attr.validators.instance_of(int))

    id: int = attr.ib(validator=attr.validators.instance_of(int))
    category: str = attr.ib(validator=attr.validators.in_(['operation', 'material']))
    cost: Money = attr.ib(converter=Money, validator=attr.validators.instance_of(Money))
    is_finish: bool = attr.ib(validator=attr.validators.instance_of(bool))
    is_outside_service: bool = attr.ib(validator=attr.validators.instance_of(bool))
    name: str = attr.ib(validator=attr.validators.instance_of(str))
    operation_definition_name: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    notes: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    position: int = attr.ib(validator=attr.validators.instance_of(int))
    quantities: List[OperationQuantity] = attr.ib(
        converter=convert_iterable(OperationQuantity)
    )
    runtime: Optional[float] = attr.ib(
        converter=optional_convert(float),
        validator=attr.validators.optional(attr.validators.instance_of(float)),
    )
    setup_time: Optional[float] = attr.ib(
        converter=optional_convert(float),
        validator=attr.validators.optional(attr.validators.instance_of(float)),
    )
    operation_definition_erp_code: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )


@attr.s(frozen=True)
class Process:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    external_name: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    name: str = attr.ib(validator=attr.validators.instance_of(str))


@attr.s(frozen=True)
class SupportingFile:
    filename: str = attr.ib(validator=attr.validators.instance_of(str))
    url: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    uuid: Optional[str] = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )


@attr.s(frozen=False)
class PurchasedComponentProperty:
    name: str = attr.ib(validator=attr.validators.instance_of(str))
    code_name: str = attr.ib(validator=attr.validators.instance_of(str))
    value_type: str = attr.ib(validator=attr.validators.instance_of(str))
    value: Optional[Union[str, float, bool]] = attr.ib()


@attr.s(frozen=False)
class PurchasedComponent:
    oem_part_number: str = attr.ib(validator=attr.validators.instance_of(str))
    piece_price: Money = attr.ib(
        converter=Money, validator=attr.validators.instance_of(Money)
    )
    properties: List[PurchasedComponentProperty] = attr.ib(
        converter=convert_iterable(PurchasedComponentProperty)
    )
    internal_part_number: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    description: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )

    def get_property(self, code_name: str) -> Optional[Union[str, float, bool]]:
        """
        Return the value of the property with the specified code name or None
        """
        return {pcp.code_name: pcp.value for pcp in self.properties}.get(
            code_name, None
        )


@attr.s(frozen=True)
class ChildComponent:
    child_id = attr.ib(validator=attr.validators.instance_of(int))
    quantity = attr.ib(validator=attr.validators.instance_of(int))


@attr.s(frozen=True)
class BaseComponent:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    child_ids: List[int] = attr.ib(converter=convert_iterable(int))
    children: List[ChildComponent] = attr.ib(converter=convert_iterable(ChildComponent))
    description: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    export_controlled: bool = attr.ib(validator=attr.validators.instance_of(bool))
    finishes: List[str] = attr.ib(converter=convert_iterable(str))
    innate_quantity: int = attr.ib(validator=attr.validators.instance_of(int))
    is_root_component: bool = attr.ib(validator=attr.validators.instance_of(bool))
    material: Material = attr.ib(converter=convert_cls(Material))
    parent_ids: List[int] = attr.ib(converter=convert_iterable(int))
    part_custom_attrs: Optional[list] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(list))
    )
    part_name: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    part_number: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    part_uuid: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    process: Process = attr.ib(converter=convert_cls(Process))
    purchased_component: PurchasedComponent = attr.ib(
        converter=convert_cls(PurchasedComponent)
    )
    revision: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    supporting_files: List[SupportingFile] = attr.ib(
        converter=convert_iterable(SupportingFile)
    )
    type: str = attr.ib(
        validator=attr.validators.in_(['assembled', 'manufactured', 'purchased'])
    )
    thumbnail_url: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )

    @property
    def is_hardware(self):
        return self.type == 'purchased'


class AssemblyComponent(NamedTuple):
    """A component with metadata describing its position in an assembly.

    Attributes:
        component   the `QuoteComponent` or `OrderComponent` instance
        level       this component's depth in the assembly tree (0 is root)
        parent      this component's parent component
        level_index index of this component within its level
        level_count count of components at this assembly level
    """

    component: Union['QuoteComponent', 'OrderComponent']
    level: int  # assembly level (0 for root)
    parent: Optional[Union['QuoteComponent', 'OrderComponent']]
    level_index: int  # 0-based index of the current component within its level
    level_count: int  # count of components at this assembly level


class AssemblyMixin:
    """Add `iterate_assembly` method for use in OrderItems and QuoteItems."""

    def iterate_assembly_with_duplicates(self) -> Generator[AssemblyComponent, None, None]:
        """Traverse assembly components in depth-first search ordering.
        Components are yielded as AssemblyComponent (namedtuple) objects,
        containing the component itself as well as information about parent
        and assembly level."""
        return self.iterate_assembly(exclude_duplicates=False)

    def iterate_assembly(self, exclude_duplicates=True) -> Generator[AssemblyComponent, None, None]:
        """Traverse assembly components in depth-first search ordering.
        Components are yielded as AssemblyComponent (namedtuple) objects,
        containing the component itself as well as information about parent
        and assembly level. The same component will only be yielded once even
        if appears twice in the assembly tree (commonly seen with
        hardware/fasteners)."""
        components_by_id = {}
        root_component = None
        for component in self.components:
            components_by_id[component.id] = component
            if component.is_root_component:
                root_component = component
        level_counter = collections.defaultdict(lambda: 0)
        visited = set()

        def dfs(node_id, level=0, parent=None):
            if exclude_duplicates:
                if node_id in visited:
                    return
                visited.add(node_id)
            node = components_by_id[node_id]
            level_index = level_counter[level]
            level_counter[level] += 1
            yield AssemblyComponent(
                component=node,
                level=level,
                parent=parent,
                level_index=level_index,
                level_count=0,
            )
            for child_id in node.child_ids:
                for y in dfs(child_id, level + 1, node):
                    yield y

        for assm_comp in list(dfs(root_component.id)):
            yield AssemblyComponent(
                component=assm_comp.component,
                level=assm_comp.level,
                parent=assm_comp.parent,
                level_index=assm_comp.level_index,
                level_count=level_counter[assm_comp.level],
            )
