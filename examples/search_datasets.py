"""Example: search and download datasets from dataset.gov.md"""
import sys
sys.path.insert(0, "..")
from src.client import MoldovaDataClient

client = MoldovaDataClient()

# ── Total count ──────────────────────────────────────────────────────────────
print(f"Total datasets: {client.count()}\n")

# ── Search by keyword ────────────────────────────────────────────────────────
keywords = ["populatie", "buget", "sanatate", "educatie", "transport"]

for kw in keywords:
    results = client.search(kw, rows=2)
    print(f"🔍 '{kw}' → {len(results)} results")
    for ds in results:
        print(f"   • {ds['title'][:70]}")
        resources = ds.get("resources", [])
        for res in resources[:1]:
            print(f"     ↳ {res.get('format','?')} — {res.get('url','')[:60]}")
    print()
