# 🍳 Recipe Vault

> A lightweight Flask web application for storing and browsing personal recipes — no database required.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x%2F3.x-black?logo=flask)](https://flask.palletsprojects.com)
[![Flasgger](https://img.shields.io/badge/API%20Docs-Swagger%20UI-85EA2D?logo=swagger)](https://github.com/flasgger/flasgger)
[![Docs](https://img.shields.io/badge/Docs-GitHub%20Pages-blue?logo=readthedocs)](https://ksak-dk.github.io/OpenSource/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📖 Project Overview

**Recipe Vault** is a minimalist recipe-management tool built with Python and Flask. Recipes are stored in a local `data.json` file, so there is no database to configure. The project demonstrates:

- Clean Flask route design with form handling and redirects
- JSON file persistence with error-safe loading
- Interactive API documentation via **Flasgger / Swagger UI**
- Auto-generated code documentation published to **GitHub Pages** via **Sphinx**

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 📋 Recipe list | Browse all recipes sorted by newest first |
| ➕ Add recipe | Submit title, category, ingredients and steps via a web form |
| 🔍 Recipe detail | View the full content of any saved recipe |
| 📑 Swagger UI | Explore and test all API endpoints interactively |
| 📚 Sphinx docs | Auto-generated HTML documentation published to GitHub Pages |

---

## 🖥️ Pages & Endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page — list all recipes |
| `/add` | GET / POST | Add-recipe form / create a new recipe |
| `/recipe/<id>` | GET | Detail page for a single recipe |
| `/apidocs/` | GET | Interactive Swagger UI (Flasgger) |

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **Flask** — web framework
- **Flasgger** — Swagger / OpenAPI documentation for Flask
- **Sphinx + sphinx-rtd-theme** — code documentation generator
- **JSON** — lightweight file-based storage (`data.json`)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or newer
- `pip`

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/ksak-dk/OpenSource.git
cd OpenSource

# 2. Create and activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the development server
python app.py
```

### Open in your browser

| URL | Description |
|-----|-------------|
| http://127.0.0.1:5000/ | Recipe list |
| http://127.0.0.1:5000/add | Add a recipe |
| http://127.0.0.1:5000/apidocs/ | Swagger UI (interactive API docs) |

---

## 📂 Project Structure

```
OpenSource/
├── app.py                      # Flask application (routes + helpers)
├── requirements.txt            # Runtime dependencies
├── data.json                   # Recipe storage (auto-created on first run)
├── templates/
│   ├── base.html               # Shared layout
│   ├── index.html              # Recipe list page
│   ├── add.html                # Add-recipe form
│   └── detail.html             # Recipe detail page
├── docs/
│   ├── conf.py                 # Sphinx configuration
│   ├── index.rst               # Documentation home
│   ├── modules.rst             # Auto-generated API reference
│   └── requirements.txt        # Documentation build dependencies
└── .github/workflows/
    └── docs.yml                # Auto-build & publish docs to GitHub Pages
```

---

## 📚 Documentation

| Resource | Link |
|----------|------|
| Sphinx code docs (GitHub Pages) | https://ksak-dk.github.io/OpenSource/ |
| Swagger / OpenAPI UI (local) | http://127.0.0.1:5000/apidocs/ |

---

## 🔧 Building the Documentation Locally

```bash
pip install -r docs/requirements.txt
sphinx-build -b html docs docs/_build/html
# Open docs/_build/html/index.html in your browser
```

---

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

> _Recipe Vault — keep your favourite recipes close at hand._