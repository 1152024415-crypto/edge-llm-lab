from __future__ import annotations

from collections.abc import Callable
from typing import Any


DEFAULT_PROPERTIES = (
    "FULL_DEVICE_NAME",
    "OPTIMIZATION_CAPABILITIES",
    "SUPPORTED_PROPERTIES",
)


def collect_openvino_devices(
    *,
    core_factory: Callable[[], Any] | None = None,
    openvino_version: str | None = None,
) -> dict[str, object]:
    errors: list[dict[str, object]] = []

    if core_factory is None or openvino_version is None:
        try:
            import openvino as ov
        except Exception as exc:
            return {
                "schema_version": 1,
                "openvino_version": None,
                "available_devices": [],
                "devices": {},
                "errors": [{"stage": "import-openvino", "error": repr(exc)}],
            }
        core_factory = core_factory or ov.Core
        openvino_version = openvino_version or getattr(ov, "__version__", "unknown")

    try:
        core = core_factory()
    except Exception as exc:
        return {
            "schema_version": 1,
            "openvino_version": openvino_version,
            "available_devices": [],
            "devices": {},
            "errors": [{"stage": "create-core", "error": repr(exc)}],
        }

    try:
        available_devices = list(core.available_devices)
    except Exception as exc:
        return {
            "schema_version": 1,
            "openvino_version": openvino_version,
            "available_devices": [],
            "devices": {},
            "errors": [{"stage": "available-devices", "error": repr(exc)}],
        }

    devices: dict[str, object] = {}
    for device in available_devices:
        properties: dict[str, object] = {}
        property_errors: list[dict[str, str]] = []
        for property_name in DEFAULT_PROPERTIES:
            try:
                properties[property_name] = to_jsonable(core.get_property(device, property_name))
            except Exception as exc:
                property_errors.append(
                    {
                        "property": property_name,
                        "error": repr(exc),
                    }
                )
        devices[device] = {
            "properties": properties,
            "property_errors": property_errors,
        }

    return {
        "schema_version": 1,
        "openvino_version": openvino_version,
        "available_devices": available_devices,
        "devices": devices,
        "errors": errors,
    }


def to_jsonable(value: Any) -> object:
    if value is None or isinstance(value, str | int | float | bool):
        return value
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [to_jsonable(item) for item in value]
    return str(value)

