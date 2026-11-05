"""Signal/slot system for inter-node communication."""

from __future__ import annotations
import inspect
import logging
from typing import Callable, Dict, List, Tuple, Any

logger = logging.getLogger("pynode.signals")


class SignalDispatcher:
    """Central signal dispatcher.  Nodes connect signals to callbacks."""

    def __init__(self, strict_validation: bool = True):
        self._connections: Dict[Tuple[int, str], List[Callable]] = {}
        self.strict_validation = strict_validation
        self._warn_count: Dict[Tuple[int, str, str], int] = {}

    def connect(self, source, signal_name: str, callback: Callable) -> None:
        key = (id(source), signal_name)
        if key not in self._connections:
            self._connections[key] = []
        self._connections[key].append(callback)
        logger.debug(f"Connected {source}.{signal_name} -> {callback.__name__}")

    def disconnect(self, source, signal_name: str, callback: Callable) -> None:
        key = (id(source), signal_name)
        if key in self._connections:
            try:
                self._connections[key].remove(callback)
            except ValueError:
                pass

    def emit(self, source, signal_name: str, *args, **kwargs) -> None:
        key = (id(source), signal_name)
        if key not in self._connections:
            return

        callbacks_to_remove = []
        for callback in list(self._connections[key]):
            try:
                if self.strict_validation:
                    sig = inspect.signature(callback)
                    params = list(sig.parameters.keys())
                    for param in params:
                        if param == "self":
                            continue
                        if param.startswith("_"):
                            continue
                        if param not in kwargs and param not in ("args", "kwargs"):
                            warn_key = (id(source), signal_name, callback.__name__)
                            count = self._warn_count.get(warn_key, 0) + 1
                            self._warn_count[warn_key] = count
                            if count >= 1:
                                logger.warning(
                                    f"Unused parameter '{param}' in callback "
                                    f"'{callback.__name__}' for signal "
                                    f"'{signal_name}'. Deregistering callback."
                                )
                                callbacks_to_remove.append(callback)
                                break

                if "shape_index" in kwargs:
                    expected_type = None
                    sig = inspect.signature(callback)
                    if "shape_index" in sig.parameters:
                        annotation = sig.parameters["shape_index"].annotation
                        if annotation is int:
                            expected_type = int
                    if expected_type is int and not isinstance(kwargs["shape_index"], int):
                        logger.warning(
                            f"Type mismatch for shape_index in "
                            f"'{callback.__name__}': expected int, got "
                            f"{type(kwargs['shape_index']).__name__}. Skipping."
                        )
                        continue

                # Build the argument list for the callback
                sig = inspect.signature(callback)
                bound_args = {}
                positional = [p for p in sig.parameters
                              if p != "self"
                              and sig.parameters[p].kind in (
                                  inspect.Parameter.POSITIONAL_ONLY,
                                  inspect.Parameter.POSITIONAL_OR_KEYWORD)]
                for i, pname in enumerate(positional):
                    if i < len(args):
                        bound_args[pname] = args[i]
                    elif pname in kwargs:
                        bound_args[pname] = kwargs[pname]
                for pname, param in sig.parameters.items():
                    if pname in bound_args or pname == "self":
                        continue
                    if pname in kwargs:
                        bound_args[pname] = kwargs[pname]
                    elif param.kind == inspect.Parameter.VAR_KEYWORD:
                        pass
                    elif param.default is not inspect.Parameter.empty:
                        pass

                callback(**bound_args)

            except Exception as exc:
                logger.error(f"Error in callback {callback.__name__}: {exc}")

        for cb in callbacks_to_remove:
            self.disconnect(source, signal_name, cb)
