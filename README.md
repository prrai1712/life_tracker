# Life Tracker · Crazy Time

Clean Flask layout that matches your original **`app.py`**: Hall of Fame (Old API), Evolution Crazy Time (New API), **Analysis**, and **`/api/*` JSON**.

---

## Requirements

- **Python 3.10+** recommended (3.9 works).

---

## Run (copy-paste)

```bash
cd "/path/to/life_tracker"

python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5001** (default).

| Env | Meaning |
|-----|---------|
| `PORT` | Listen port (default `5001`) |
| `FLASK_DEBUG` | `false` disables the debugger |
| `CASINO_OLD_API_URL`, `CASINO_NEW_API_URL` | Override endpoints |
| `USD_TO_INR_RATE`, `EUR_TO_INR_RATE` | Conversion rates |

---

## Routes

| URL | Purpose |
|-----|---------|
| `/` | Dashboard |
| `/analysis` | Player totals from current Crazy Time slice |
| `/api/games` | Same data as `/` as JSON |
| `/api/analysis` | Same data as `/analysis` as JSON |

---

## Layout

```
app.py
config/constants.py      # URLs, headers, currencies, defaults
services/casino_client.py # requests wrapper
services/old_api_service.py
services/new_api_service.py
services/analysis_service.py
routes/{home,analysis,api}_routes.py
utils/helper.py           # clean_text + query parsing
templates/ …
static/css/style.css
static/js/app.js
```
