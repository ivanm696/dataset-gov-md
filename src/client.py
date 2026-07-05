"""
Moldova Open Data Client
CKAN 2.10.4 API wrapper for dataset.gov.md
Author: Ivan Melenciuc <melenciucivan03@gmail.com>
"""
import urllib.request
import urllib.parse
import json
from typing import Optional

BASE_URL = "https://dataset.gov.md/api/3/action"


def _get(action: str, params: dict = {}) -> dict:
    url = f"{BASE_URL}/{action}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=15) as r:
        data = json.loads(r.read().decode())
    if not data.get("success"):
        raise RuntimeError(f"CKAN error: {data.get('error')}")
    return data["result"]


class MoldovaDataClient:
    """Client for dataset.gov.md CKAN API. No API key required."""

    def status(self) -> dict:
        """Check API status and CKAN version."""
        return _get("status_show")

    def count(self) -> int:
        """Total number of datasets."""
        return _get("package_search", {"rows": 0})["count"]

    def search(self, query: str, rows: int = 10, start: int = 0) -> list[dict]:
        """Search datasets by keyword."""
        result = _get("package_search", {"q": query, "rows": rows, "start": start})
        return result["results"]

    def list_datasets(self, limit: int = 100) -> list[str]:
        """Return list of all dataset IDs."""
        return _get("package_list", {"limit": limit})

    def get_dataset(self, dataset_id: str) -> dict:
        """Get full metadata for a dataset by ID."""
        return _get("package_show", {"id": dataset_id})

    def list_organizations(self) -> list[str]:
        """Return list of all organization IDs."""
        return _get("organization_list")

    def get_organization(self, org_id: str) -> dict:
        """Get organization details."""
        return _get("organization_show", {"id": org_id, "include_datasets": True})

    def org_datasets(self, org_id: str, rows: int = 20) -> list[dict]:
        """Get datasets from a specific organization."""
        result = _get("package_search", {"fq": f"organization:{org_id}", "rows": rows})
        return result["results"]

    def list_groups(self) -> list[str]:
        """Return list of topic groups."""
        return _get("group_list")

    def recent(self, rows: int = 10) -> list[dict]:
        """Get most recently updated datasets."""
        result = _get("package_search", {
            "sort": "metadata_modified desc",
            "rows": rows
        })
        return result["results"]

    def resources(self, dataset_id: str) -> list[dict]:
        """Get downloadable resources for a dataset."""
        ds = self.get_dataset(dataset_id)
        return ds.get("resources", [])


if __name__ == "__main__":
    client = MoldovaDataClient()

    print("=== Moldova Open Data Portal ===")
    status = client.status()
    print(f"CKAN version : {status['ckan_version']}")
    print(f"Total datasets: {client.count()}")

    print("\n--- Search: 'agricultură' ---")
    for ds in client.search("agricultură", rows=3):
        print(f"  [{ds['name']}] {ds['title']}")

    print("\n--- Recent datasets ---")
    for ds in client.recent(rows=3):
        print(f"  {ds['metadata_modified'][:10]}  {ds['title'][:60]}")
