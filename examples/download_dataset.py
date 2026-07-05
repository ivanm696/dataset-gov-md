"""Example: get dataset metadata and download resources."""
import urllib.request
from client import MoldovaDataClient

client = MoldovaDataClient()

# Get dataset metadata by name
dataset = client.get_dataset("populatia-republicii-moldova")

print(f"Title:        {dataset.get('title')}")
print(f"Organization: {dataset.get('organization', {}).get('title')}")
print(f"License:      {dataset.get('license_title')}")
print(f"Resources:    {len(dataset.get('resources', []))}")

# List downloadable resources
for r in dataset.get("resources", []):
    name   = r.get("name") or r.get("description") or "resource"
    fmt    = r.get("format", "?")
    url    = r.get("url", "")
    size   = r.get("size") or "?"
    print(f"\n  📁 {name} ({fmt}, {size} bytes)")
    print(f"     {url}")

    # Download first CSV/JSON resource
    if fmt.upper() in ("CSV", "JSON") and url:
        filename = url.split("/")[-1] or f"resource.{fmt.lower()}"
        print(f"  ⬇  Downloading → {filename}")
        urllib.request.urlretrieve(url, filename)
        print(f"  ✅ Saved {filename}")
        break
