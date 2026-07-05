"""Example: search datasets by keyword and organization."""
from client import MoldovaDataClient

client = MoldovaDataClient()

# 1. Total count
print(f"Total datasets: {client.count()}")

# 2. Search by keyword
results = client.search("agricultură", rows=5)
client.print_results(results)

# 3. Search by organization
results = client.search_by_organization("ministerul-finantelor", rows=5)
client.print_results(results)

# 4. Search with tag filter
results = client.search("", rows=5, tags=["statistica"])
client.print_results(results)
