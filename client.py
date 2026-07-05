"""
Moldova Open Data Client
========================
Python client for dataset.gov.md CKAN Action API.
No API key required for read endpoints.

Usage:
    from client import MoldovaDataClient
    client = MoldovaDataClient()
    results = client.search("agricultură")
"""

import json
import urllib.request
import urllib.parse
from typing import Optional


BASE_URL = "https://dataset.gov.md/api/3/action"


class MoldovaDataClient:
    """Simple client for dataset.gov.md CKAN Action API."""

    def __init__(self, base_url: str = BASE_URL, timeout: int = 15):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _get(self, action: str, params: Optional[dict] = None) -> dict:
        url = f"{self.base_url}/{action}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        with urllib.request.urlopen(url, timeout=self.timeout) as resp:
            data = json.loads(resp.read().decode())
        if not data.get("success"):
            raise RuntimeError(f"CKAN error: {data.get('error')}")
        return data["result"]

    # ── Dataset search ────────────────────────────────────────────────────────

    def search(self, query: str = "", rows: int = 20, start: int = 0,
               organization: Optional[str] = None,
               tags: Optional[list] = None) -> dict:
        """Search datasets. Returns {'count': int, 'results': list}."""
        fq_parts = []
        if organization:
            fq_parts.append(f"organization:{organization}")
        if tags:
            fq_parts.append(" ".join(f"tags:{t}" for t in tags))

        params = {"q": query, "rows": rows, "start": start}
        if fq_parts:
            params["fq"] = " ".join(fq_parts)

        return self._get("package_search", params)

    def count(self) -> int:
        """Total number of datasets in the catalog."""
        return self.search(rows=0)["count"]

    # ── Dataset detail ────────────────────────────────────────────────────────

    def get_dataset(self, name_or_id: str) -> dict:
        """Get full metadata for a single dataset."""
        return self._get("package_show", {"id": name_or_id})

    def list_datasets(self, limit: int = 100, offset: int = 0) -> list:
        """List dataset name/id strings."""
        return self._get("package_list", {"limit": limit, "offset": offset})

    # ── Organizations ─────────────────────────────────────────────────────────

    def list_organizations(self) -> list:
        """List all organization name strings."""
        return self._get("organization_list")

    def get_organization(self, name_or_id: str, include_datasets: bool = False) -> dict:
        """Get organization detail."""
        return self._get("organization_show", {
            "id": name_or_id,
            "include_datasets": include_datasets,
        })

    def search_by_organization(self, organization: str, rows: int = 20) -> dict:
        """Search datasets belonging to a specific organization."""
        return self.search(organization=organization, rows=rows)

    # ── Groups / tags ─────────────────────────────────────────────────────────

    def list_groups(self) -> list:
        return self._get("group_list")

    def list_tags(self) -> list:
        return self._get("tag_list")

    # ── Status ────────────────────────────────────────────────────────────────

    def status(self) -> dict:
        """CKAN instance status (version, extensions, etc.)."""
        return self._get("status_show")

    # ── Helpers ───────────────────────────────────────────────────────────────

    def print_results(self, results: dict, max_rows: int = 10) -> None:
        """Pretty-print search results."""
        total = results.get("count", 0)
        items = results.get("results", [])
        print(f"\n📊 Found {total} datasets (showing {min(len(items), max_rows)}):\n")
        for i, ds in enumerate(items[:max_rows], 1):
            title = ds.get("title") or ds.get("name", "—")
            org   = ds.get("organization", {}).get("title", "—") if ds.get("organization") else "—"
            fmt   = ", ".join(
                r.get("format", "?") for r in ds.get("resources", []) if r.get("format")
            ) or "—"
            print(f"  {i:>2}. {title}")
            print(f"      🏛  {org}  |  📁 {fmt}")
        print()


# ── CLI demo ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    client = MoldovaDataClient()

    print("=" * 60)
    print("  dataset.gov.md — Moldova Open Data Client")
    print("=" * 60)

    # 1. Total count
    total = client.count()
    print(f"\n✅ Catalog is live — {total} datasets available\n")

    # 2. CKAN version
    st = client.status()
    print(f"📦 CKAN version : {st.get('ckan_version')}")
    print(f"🌐 Site URL     : {st.get('site_url')}")

    # 3. Search examples
    demos = [
        ("agricultură",    None),
        ("mediu",          None),
        ("statistica",     None),
        ("",               "ministerul-finantelor"),
    ]

    for q, org in demos:
        label = f'"{q}"' if q else f"org={org}"
        print(f"\n🔍 Searching {label}…")
        res = client.search(q, rows=5, organization=org)
        client.print_results(res, max_rows=5)
