"""Common interface for all job sources."""

from typing import Protocol, List, runtime_checkable

from agent.models import Listing, SearchQuery


@runtime_checkable
class JobSource(Protocol):
    """Every source must search and return normalized Listing objects."""

    name: str

    def search(self, query: SearchQuery) -> List[Listing]:
        """Return listings matching the query (may be empty on failure)."""
        ...
