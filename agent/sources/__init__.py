"""Job source adapters — all return normalized Listing objects."""

from agent.sources.base import JobSource
from agent.sources.demo import DemoSource
from agent.sources.remotive import RemotiveSource
from agent.sources.remoteok import RemoteOKSource

__all__ = ["JobSource", "DemoSource", "RemotiveSource", "RemoteOKSource"]
