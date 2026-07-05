"""Example: find and download a specific dataset resource"""
import sys, os, urllib.request
sys.path.insert(0, "..")
from src.client import MoldovaDataClient

client = MoldovaDataClient()

# Search for population data
results = client.search("populatie raioane", rows=5)

for ds in results:
    print(f"\n📦 {ds['title']}")
    print(f"   ID: {ds['name']}")
    for res in ds.get("resources", []):
        fmt = res.get("format", "").upper()
        url = res.get("url", "")
        name = res.get("name", "resource")
        print(f"   [{fmt}] {name[:50]} → {url[:70]}")
