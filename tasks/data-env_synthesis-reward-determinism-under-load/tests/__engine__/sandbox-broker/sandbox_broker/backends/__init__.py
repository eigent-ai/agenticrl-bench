from __future__ import annotations
import importlib
from .base import (NETWORK_EGRESS, NETWORK_MODES, NETWORK_NONE, Backend, CreateSpec, ExecOutcome, FileTooLarge,
                   ImageBuildError, ImageSpec)
REGISTRY: dict[str, str] = {
    "modal": "sandbox_broker.backends.modal_backend:ModalBackend",
    "daytona": "sandbox_broker.backends.daytona_backend:DaytonaBackend",
    "harbor": "sandbox_broker.backends.harbor_backend:HarborBackend",
    "local": "sandbox_broker.backends.local:LocalBackend",
}
def load_backend_class(name: str) -> type[Backend]:
    try:
        target = REGISTRY[name]
    except KeyError:
        raise ValueError(f"unknown backend {name!r}; known: {', '.join(sorted(REGISTRY))}") from None
    module, _, attr = target.partition(":")
    return getattr(importlib.import_module(module), attr)
__all__ = ["Backend", "CreateSpec", "ExecOutcome", "FileTooLarge", "ImageBuildError", "ImageSpec", "NETWORK_EGRESS",
           "NETWORK_MODES", "NETWORK_NONE", "REGISTRY", "load_backend_class"]
