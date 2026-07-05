# 🇲🇩 dataset.gov.md — Portalul Datelor Deschise

> Moldova's national open-data catalog — **CKAN 2.10.4** — ~1,275 government datasets

[![API Health](https://github.com/ivanm696/dataset-gov-md/actions/workflows/api-health.yml/badge.svg)](https://github.com/ivanm696/dataset-gov-md/actions/workflows/api-health.yml)

**Portal:** https://dataset.gov.md  
**API Base:** `https://dataset.gov.md/api/3/action`  
**Datasets:** ~1,275 | **No API key required** for read endpoints

---

## Quick Start

```bash
git clone https://github.com/ivanm696/dataset-gov-md.git
cd dataset-gov-md
python client.py
```

## Python Client

```python
from client import MoldovaDataClient

client = MoldovaDataClient()

# Total datasets
print(client.count())  # → 1275

# Search by keyword
results = client.search("agricultură", rows=10)
client.print_results(results)

# Search by organization
results = client.search_by_organization("ministerul-finantelor")
client.print_results(results)

# Get dataset metadata
ds = client.get_dataset("populatia-republicii-moldova")
print(ds["title"], ds["resources"])

# List organizations
orgs = client.list_organizations()

# CKAN status
status = client.status()
print(status["ckan_version"])  # → 2.10.4
```

## API Reference

| Method | Description |
|---|---|
| `search(query, rows, organization, tags)` | Search datasets |
| `count()` | Total dataset count |
| `get_dataset(name_or_id)` | Full dataset metadata |
| `list_datasets()` | All dataset names |
| `list_organizations()` | All organization names |
| `get_organization(name)` | Organization detail |
| `search_by_organization(org)` | Datasets by org |
| `list_tags()` | All tags |
| `status()` | CKAN instance info |

## Direct API Examples

```bash
# Total count
curl "https://dataset.gov.md/api/3/action/package_search?rows=0"

# Search datasets
curl "https://dataset.gov.md/api/3/action/package_search?q=agricultura&rows=5"

# By organization
curl "https://dataset.gov.md/api/3/action/package_search?fq=organization:ministerul-finantelor"

# Dataset detail
curl "https://dataset.gov.md/api/3/action/package_show?id=populatia-republicii-moldova"

# All organizations
curl "https://dataset.gov.md/api/3/action/organization_list"

# CKAN version
curl "https://dataset.gov.md/api/3/action/status_show"
```

## Key Organizations

| Organization | Datasets |
|---|---|
| Biroul Național de Statistică | ~300 |
| Ministerul Finanțelor | ~150 |
| Ministerul Economiei | ~80 |
| Ministerul Agriculturii | ~60 |
| Ministerul Sănătății | ~50 |

## Examples

```bash
python examples/search_datasets.py      # keyword + org search
python examples/download_dataset.py    # get metadata + download CSV
python examples/list_organizations.py  # list all organizations
```

## Project Structure

```
dataset-gov-md/
├── client.py              # Python API client (zero dependencies)
├── apis.yml               # APIs.json catalog spec
├── review.yml             # Live API verification log
├── requirements.txt
├── examples/
│   ├── search_datasets.py
│   ├── download_dataset.py
│   └── list_organizations.py
└── .github/workflows/
    └── api-health.yml     # Weekly health check (Mondays)
```

## Notes

- **API lives on `dataset.gov.md`**, not `date.gov.md` (landing portal)
- All `/ckan/` and `/api/3/` paths on `date.gov.md` return 404
- Live endpoint verified: `package_search?rows=0` → count=1,275, HTTP 200
- CKAN docs: https://docs.ckan.org/en/2.10/api/

## Maintainer

**Ivan Melenciuc** — melenciucivan03@gmail.com  
GitHub: [@ivanm696](https://github.com/ivanm696)

## License

MIT
