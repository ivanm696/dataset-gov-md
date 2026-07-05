# 🇲🇩 dataset.gov.md — Portalul Datelor Deschise Moldova

[![API Health](https://github.com/ivanm696/dataset-gov-md/actions/workflows/api-health.yml/badge.svg)](https://github.com/ivanm696/dataset-gov-md/actions/workflows/api-health.yml)
![Datasets](https://img.shields.io/badge/datasets-1275%2B-blue)
![CKAN](https://img.shields.io/badge/CKAN-2.10.4-orange)
![License](https://img.shields.io/badge/license-Open%20Data-green)

Каталог API для национального портала открытых данных Республики Молдова.
Работает на **CKAN 2.10.4**, ~1275 датасетов, **API ключ не нужен**.

**Портал:** https://dataset.gov.md  
**API Base:** `https://dataset.gov.md/api/3/action`  
**Документация CKAN:** https://docs.ckan.org/en/2.10/api/

---

## 🚀 Быстрый старт

### curl

```bash
# Статус API
curl "https://dataset.gov.md/api/3/action/status_show"

# Количество датасетов
curl "https://dataset.gov.md/api/3/action/package_search?rows=0"

# Поиск по ключевому слову
curl "https://dataset.gov.md/api/3/action/package_search?q=populatie&rows=5"

# Список организаций
curl "https://dataset.gov.md/api/3/action/organization_list"

# Информация о конкретном датасете
curl "https://dataset.gov.md/api/3/action/package_show?id=DATASET_ID"
```

### Python (без зависимостей)

```python
from src.client import MoldovaDataClient

client = MoldovaDataClient()

# Общая статистика
print(client.count())            # → 1275

# Поиск датасетов
results = client.search("populatie", rows=5)
for ds in results:
    print(ds["title"])

# Последние обновления
for ds in client.recent(rows=5):
    print(ds["metadata_modified"][:10], ds["title"])

# Ресурсы для скачивания
resources = client.resources("DATASET_ID")
for r in resources:
    print(r["format"], r["url"])

# Датасеты по организации
datasets = client.org_datasets("ministerul-finantelor")
```

---

## 📊 Примеры датасетов по темам

| Тема | Ключевое слово | Примерные датасеты |
|---|---|---|
| 👥 Население | `populatie` | Население по районам, перепись |
| 💰 Бюджет | `buget` | Бюджет государства, расходы |
| 🏥 Здоровье | `sanatate` | Больницы, заболеваемость |
| 🎓 Образование | `educatie` | Школы, университеты |
| 🚗 Транспорт | `transport` | Дороги, автопарк |
| 🌾 Сельское хозяйство | `agricultura` | Урожайность, площади |
| ⚖️ Юстиция | `justitie` | Суды, преступность |
| 🏛️ Администрация | `administratie` | Госорганы, решения |

---

## 🛠️ Структура репозитория

```
dataset-gov-md/
├── src/
│   └── client.py           # Python клиент (без зависимостей)
├── examples/
│   ├── search_datasets.py  # Поиск датасетов по темам
│   ├── list_organizations.py # Список организаций с количеством
│   └── download_resource.py  # Нахождение и скачивание ресурсов
├── .github/workflows/
│   └── api-health.yml      # Еженедельная проверка API (каждый понедельник)
├── apis.yml                # APIs.json спецификация
├── review.yml              # Результаты верификации API
└── README.md
```

---

## 📡 API Endpoints

| Endpoint | Описание |
|---|---|
| `status_show` | Статус CKAN, версия |
| `package_search?q=...` | Поиск датасетов |
| `package_list` | Все ID датасетов |
| `package_show?id=...` | Метаданные датасета |
| `organization_list` | Все организации |
| `organization_show?id=...` | Детали организации |
| `group_list` | Тематические группы |

---

## 🔗 Полезные ссылки

- 🌐 [Портал dataset.gov.md](https://dataset.gov.md)
- 📖 [Документация CKAN API](https://docs.ckan.org/en/2.10/api/)
- 🇲🇩 [date.gov.md](https://date.gov.md) — лендинг портал
- 📊 [CKAN Action API Reference](https://docs.ckan.org/en/2.10/api/#action-api-reference)

---

## 👤 Maintainer

**Ivan Melenciuc** · melenciucivan03@gmail.com  
GitHub: [@ivanm696](https://github.com/ivanm696)
