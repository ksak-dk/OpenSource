# Recipe Vault (Flask)

A simple Flask mini-project with **3 pages**:
- Home (recipe list)
- Add Recipe (form)
- Recipe Detail

## Features (Pages)
1. `/` - List recipes
2. `/add` - Add a new recipe
3. `/recipe/<id>` - View recipe detail

## Tech
- Python
- Flask
- JSON file storage (`data.json`)

## Setup & Run
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open:
- http://127.0.0.1:5000/