from flask import Flask, render_template, request, redirect, url_for, abort
import json
import os
from datetime import datetime
from uuid import uuid4

app = Flask(__name__)

DATA_FILE = "data.json"


def load_recipes():
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


def save_recipes(recipes):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(recipes, f, ensure_ascii=False, indent=2)


@app.route("/")
def index():
    recipes = load_recipes()
    recipes = sorted(recipes, key=lambda r: r.get("created_at", ""), reverse=True)
    return render_template("index.html", recipes=recipes)


@app.route("/add", methods=["GET", "POST"])
def add_recipe():
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
        new_recipe = {
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
def recipe_detail(recipe_id):
    recipes = load_recipes()
    recipe = next((r for r in recipes if r.get("id") == recipe_id), None)
    if not recipe:
        abort(404)
    return render_template("detail.html", recipe=recipe)


if __name__ == "__main__":
    app.run(debug=True)