"""Example: list all organizations and their dataset counts"""
import sys
sys.path.insert(0, "..")
from src.client import MoldovaDataClient

client = MoldovaDataClient()
orgs = client.list_organizations()
print(f"Total organizations: {len(orgs)}\n")

for org_id in orgs[:15]:
    try:
        datasets = client.org_datasets(org_id, rows=1)
        # Get full count
        import urllib.request, urllib.parse, json
        url = f"https://dataset.gov.md/api/3/action/package_search?fq=organization:{org_id}&rows=0"
        with urllib.request.urlopen(url, timeout=10) as r:
            count = json.loads(r.read())["result"]["count"]
        print(f"  [{count:3d}] {org_id}")
    except Exception:
        print(f"  [???] {org_id}")
