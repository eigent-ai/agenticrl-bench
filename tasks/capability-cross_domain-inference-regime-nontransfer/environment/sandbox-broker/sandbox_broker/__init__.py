"""Sandbox gate: a platform-neutral local service for short-lived task sandboxes.

A root daemon holds the platform credentials and creates sandboxes (no network unless the
operator's policy says otherwise) on request over a Unix socket. Workloads use the
``sandbox`` command (``sandbox_broker.cli``), the clients in ``sandbox_broker.client`` or the
Harbor environment ``sandbox_broker.harbor_env:BrokerEnvironment``; none of them expose the
platform or its credentials. The package keeps its historical name ``sandbox_broker``.
"""
__version__ = "0.2.0"

from .client import AsyncBrokerClient, AsyncSandbox, BrokerClient, ExecResult, Sandbox  # noqa: E402
from .protocol import (BackendFailure, BadRequest, BrokerError, BrokerUnavailable, PolicyDenied,  # noqa: E402
                       QuotaExceeded, SandboxNotFound)

__all__ = [
    "AsyncBrokerClient", "AsyncSandbox", "BrokerClient", "ExecResult", "Sandbox",
    "BackendFailure", "BadRequest", "BrokerError", "BrokerUnavailable", "PolicyDenied", "QuotaExceeded",
    "SandboxNotFound", "__version__",
]
