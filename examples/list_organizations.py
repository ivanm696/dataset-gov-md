"""Example: list all organizations and their dataset counts."""
from client import MoldovaDataClient

client = MoldovaDataClient()

orgs = client.list_organizations()
print(f"Total organizations: {len(orgs)}\n")

# Show first 20
for name in orgs[:20]:
    try:
        org = client.get_organization(name)
        count = org.get("package_count", "?")
        title = org.get("title") or name
        print(f"  {count:>4}  {title}")
    except Exception:
        print(f"     ?  {name}")
