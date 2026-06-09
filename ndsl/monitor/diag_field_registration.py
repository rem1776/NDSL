from collections.abc import Mapping
from dataclasses import Field
from datetime import datetime
from typing import Any


def register_diag_manager_fields(
    *,
    dataclass_fields: Mapping[str, Field[Any]],
    monitor: Any,
    init_time: datetime,
    field_names: list[str],
    module_name: str,
    dtype: Any,
    use_metadata_name: bool = False,
) -> None:
    """Register selected dataclass fields with the diag_manager monitor.

    The input list is updated in place by removing any names that are registered.
    """
    for field_name in list(field_names):
        dataclass_field = dataclass_fields.get(field_name)
        if dataclass_field is None:
            continue

        dims = dataclass_field.metadata.get("dims", "unknown")
        units = dataclass_field.metadata.get("units", "unknown")
        if use_metadata_name:
            diag_field_name = dataclass_field.metadata.get("name", field_name)
        else:
            diag_field_name = field_name

        monitor.register_field(
            module_name=module_name,
            field_name=diag_field_name,
            dims=dims,
            units=units,
            init_time=init_time,
            dtype=dtype,
        )
        field_names.remove(field_name)