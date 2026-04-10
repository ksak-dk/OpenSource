"""Recipe Vault Flask Application.

A simple web application for managing personal recipes. Supports listing,
adding, and viewing recipe details. Data is persisted to a local JSON file.

Example:
    To start the development server::

        $ python app.py

    Then open http://127.0.0.1:5000/ in your browser.
"""

from flask import Flask, render_template, request, redirect, url_for, abort
from flasgger import Swagger
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from uuid import uuid4

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Swagger / OpenAPI configuration
# ---------------------------------------------------------------------------
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
}

swagger_template = {
    "info": {
        "title": "Recipe Vault API",
        "description": (
            "Interactive API documentation for the Recipe Vault Flask application. "
            "Use the endpoints below to list, add, and view recipes."
        ),
        "version": "1.0.0",
        "contact": {"name": "Recipe Vault"},
    },
    "tags": [
        {"name": "recipes", "description": "Recipe management operations"},
    ],
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

DATA_FILE = "data.json"


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------


def load_recipes() -> List[Dict[str, Any]]:
    """Load all recipes from the JSON data file.

    Reads ``DATA_FILE`` and returns its contents as a list of recipe
    dictionaries.  Returns an empty list when the file does not exist or
    contains invalid JSON.

    Returns:
        List[Dict[str, Any]]: A list of recipe dictionaries.  Each dictionary
        contains at minimum the keys ``id``, ``title``, ``category``,
        ``ingredients``, ``steps``, and ``created_at``.

    Example:
        >>> recipes = load_recipes()
        >>> isinstance(recipes, list)
        True
    """
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
        except json.JSONDecodeError:
            return []


def save_recipes(recipes: List[Dict[str, Any]]) -> None:
    """Persist the recipe list to the JSON data file.

    Serialises *recipes* to ``DATA_FILE`` using UTF-8 encoding and a
    2-space indent for human-readable output.

    Args:
        recipes (List[Dict[str, Any]]): The list of recipe dictionaries to
            save.  The list replaces any existing content in ``DATA_FILE``.

    Example:
        >>> save_recipes([{"id": "abc12345", "title": "Pasta"}])
    """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(recipes, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.route("/")
def index():
    """Render the recipe list page.

    Loads all recipes from storage, sorts them newest-first, and renders the
    ``index.html`` template.

    ---
    tags:
      - recipes
    summary: List all recipes
    description: Returns an HTML page displaying all stored recipes sorted by creation date (newest first).
    responses:
      200:
        description: HTML page with the recipe list.
    """
    recipes = load_recipes()
    # newest first
    recipes = sorted(recipes, key=lambda r: r.get("created_at", ""), reverse=True)
    return render_template("index.html", recipes=recipes)


@app.route("/add", methods=["GET", "POST"])
def add_recipe():
    """Render the add-recipe form (GET) or create a new recipe (POST).

    **GET** – returns the empty add-recipe form.

    **POST** – validates the submitted form data, creates a new recipe
    dictionary with a randomly-generated 8-character ID, appends it to
    storage, and redirects to the recipe detail page.

    ---
    tags:
      - recipes
    summary: Add a new recipe
    description: >
      GET returns the recipe submission form.
      POST validates form data and persists a new recipe, then redirects to
      the detail page for the newly created recipe.
    consumes:
      - application/x-www-form-urlencoded
    parameters:
      - in: formData
        name: title
        type: string
        required: true
        description: Recipe title (must not be blank).
      - in: formData
        name: category
        type: string
        required: false
        description: Recipe category (e.g. Main, Dessert).  Defaults to "Uncategorized".
      - in: formData
        name: ingredients
        type: string
        required: false
        description: Ingredients list (free-form text).
      - in: formData
        name: steps
        type: string
        required: false
        description: Preparation steps (free-form text).
    responses:
      200:
        description: Add-recipe form (GET) or form with validation error (POST).
      302:
        description: Redirect to the new recipe's detail page on success.
    """
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        ingredients = request.form.get("ingredients", "").strip()
        steps = request.form.get("steps", "").strip()

        if not title:
            return render_template(
                "add.html",
                error="Title is required.",
                form=request.form
            )

        recipes = load_recipes()
        new_recipe: Dict[str, Any] = {
            "id": str(uuid4())[:8],
            "title": title,
            "category": category or "Uncategorized",
            "ingredients": ingredients,
            "steps": steps,
            "created_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        }
        recipes.append(new_recipe)
        save_recipes(recipes)
        return redirect(url_for("recipe_detail", recipe_id=new_recipe["id"]))

    return render_template("add.html", error=None, form={})


@app.route("/recipe/<recipe_id>")
def recipe_detail(recipe_id: str):
    """Render the detail page for a single recipe.

    Looks up *recipe_id* in the stored recipes list and renders the
    ``detail.html`` template.  Returns HTTP 404 when no matching recipe is
    found.

    Args:
        recipe_id (str): The 8-character unique identifier of the recipe.

    ---
    tags:
      - recipes
    summary: View a recipe's detail page
    description: Returns an HTML page with the full details of a single recipe identified by its ID.
    parameters:
      - in: path
        name: recipe_id
        type: string
        required: true
        description: The unique 8-character ID of the recipe.
    responses:
      200:
        description: HTML page with the recipe details.
      404:
        description: Recipe not found.
    """
    recipes = load_recipes()
    recipe: Optional[Dict[str, Any]] = next(
        (r for r in recipes if r.get("id") == recipe_id), None
    )
    if not recipe:
        abort(404)
    return render_template("detail.html", recipe=recipe)


if __name__ == "__main__":
    app.run(debug=True)