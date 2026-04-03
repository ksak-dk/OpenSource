"""
Pytest tests for app.py (Recipe Vault).

Uses Flask's built-in test client and a temporary data file so tests are
isolated from each other and from any real data.json on disk.
"""

import json
import os
import pytest

import app as application


@pytest.fixture()
def client(tmp_path, monkeypatch):
    """Return a Flask test client that writes data to a temp directory."""
    data_file = str(tmp_path / "data.json")
    monkeypatch.setattr(application, "DATA_FILE", data_file)
    application.app.config["TESTING"] = True
    with application.app.test_client() as c:
        yield c


# ---------------------------------------------------------------------------
# load_recipes / save_recipes helpers
# ---------------------------------------------------------------------------

def test_load_recipes_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(application, "DATA_FILE", str(tmp_path / "missing.json"))
    assert application.load_recipes() == []


def test_load_recipes_empty_file(tmp_path, monkeypatch):
    f = tmp_path / "data.json"
    f.write_text("")
    monkeypatch.setattr(application, "DATA_FILE", str(f))
    assert application.load_recipes() == []


def test_save_and_load_round_trip(tmp_path, monkeypatch):
    f = tmp_path / "data.json"
    monkeypatch.setattr(application, "DATA_FILE", str(f))
    recipes = [{"id": "abc", "title": "Soup"}]
    application.save_recipes(recipes)
    assert application.load_recipes() == recipes


# ---------------------------------------------------------------------------
# build_recipe helper
# ---------------------------------------------------------------------------

def test_build_recipe_sets_required_fields():
    recipe = application.build_recipe("Soup", "", "", "")
    assert recipe["title"] == "Soup"
    assert recipe["category"] == "Uncategorized"
    assert "id" in recipe
    assert "created_at" in recipe


def test_build_recipe_uses_provided_category():
    recipe = application.build_recipe("Soup", "Starter", "", "")
    assert recipe["category"] == "Starter"


def test_build_recipe_stores_ingredients_and_steps():
    recipe = application.build_recipe("Soup", "", "water\nsalt", "Boil it")
    assert recipe["ingredients"] == "water\nsalt"
    assert recipe["steps"] == "Boil it"


def test_build_recipe_unique_ids():
    ids = {application.build_recipe(f"Recipe {i}", "", "", "")["id"] for i in range(10)}
    assert len(ids) == 10


# ---------------------------------------------------------------------------
# GET /
# ---------------------------------------------------------------------------

def test_index_returns_200(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_index_shows_no_recipes_message(client):
    resp = client.get("/")
    assert b"No recipes yet" in resp.data


def test_index_lists_recipes(client):
    application.save_recipes([
        {"id": "a1", "title": "Apple Pie", "category": "Dessert",
         "ingredients": "", "steps": "", "created_at": "2024-01-01T00:00:00Z"},
    ])
    resp = client.get("/")
    assert b"Apple Pie" in resp.data


def test_index_newest_first(client):
    application.save_recipes([
        {"id": "old", "title": "Old Soup", "category": "Main",
         "ingredients": "", "steps": "", "created_at": "2024-01-01T00:00:00Z"},
        {"id": "new", "title": "New Salad", "category": "Main",
         "ingredients": "", "steps": "", "created_at": "2025-06-01T00:00:00Z"},
    ])
    resp = client.get("/")
    html = resp.data.decode()
    assert html.index("New Salad") < html.index("Old Soup")


# ---------------------------------------------------------------------------
# GET /add
# ---------------------------------------------------------------------------

def test_add_get_returns_200(client):
    resp = client.get("/add")
    assert resp.status_code == 200


def test_add_get_shows_form(client):
    resp = client.get("/add")
    assert b"<form" in resp.data


# ---------------------------------------------------------------------------
# POST /add
# ---------------------------------------------------------------------------

def test_add_post_requires_title(client):
    resp = client.post("/add", data={"title": "", "category": ""})
    assert resp.status_code == 200
    assert b"Title is required" in resp.data


def test_add_post_valid_redirects_to_detail(client):
    resp = client.post(
        "/add",
        data={"title": "Garlic Rice", "category": "Main",
              "ingredients": "rice\ngarlic", "steps": "Cook"},
        follow_redirects=False,
    )
    assert resp.status_code == 302
    assert "/recipe/" in resp.headers["Location"]


def test_add_post_saves_recipe(client):
    client.post(
        "/add",
        data={"title": "Garlic Rice", "category": "Main",
              "ingredients": "rice\ngarlic", "steps": "Cook"},
    )
    recipes = application.load_recipes()
    assert len(recipes) == 1
    assert recipes[0]["title"] == "Garlic Rice"


def test_add_post_default_category(client):
    client.post("/add", data={"title": "Mystery Dish", "category": ""})
    recipes = application.load_recipes()
    assert recipes[0]["category"] == "Uncategorized"


# ---------------------------------------------------------------------------
# GET /recipe/<id>
# ---------------------------------------------------------------------------

def test_recipe_detail_returns_200(client):
    application.save_recipes([
        {"id": "abc123", "title": "Tacos", "category": "Main",
         "ingredients": "beef", "steps": "Grill", "created_at": "2024-01-01T00:00:00Z"},
    ])
    resp = client.get("/recipe/abc123")
    assert resp.status_code == 200
    assert b"Tacos" in resp.data


def test_recipe_detail_404_for_missing(client):
    resp = client.get("/recipe/doesnotexist")
    assert resp.status_code == 404
